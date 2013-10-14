# vim: set fileencoding=utf-8 :
from . import matchers
from .functionlist import FunctionList
from .config import Config, ConfigAttribute
from .logs import setup_logging
from .script_handler import ScriptHandler
from .result import Result
import os
import signal
import logging
import json


logger = logging.getLogger(__name__)


class Roac(object):
    """The Roac object implements the execution of scripts in a timed loop,
    reading said scripts and executing callbacks when necessary. It manages
    the life cycle of a Roäc application
    """

    default_config = {
        'script_dir': 'scripts',
        'interval': 30,
        'debug': False,
        'script_timeout': 5
    }

    interval = ConfigAttribute('interval')
    script_dir = ConfigAttribute('script_dir')
    debug = ConfigAttribute('debug')
    script_timeout = ConfigAttribute('script_timeout')

    def __init__(self, script_class=None, **kwargs):
        if script_class is None:
            from .script import Script
            self.script_class = Script
        else:
            self.script_class = script_class
        self.config = Config(self.default_config)
        self.config.update(kwargs)
        self.script_handlers = []
        self.before_execution_functions = FunctionList(
            catch_exceptions=not self.debug)
        self.after_handler_functions = FunctionList(
            catch_exceptions=not self.debug)
        setup_logging(self)

    def before_excecution(self, f):
        """Registers a function to be called before running scripts.
        It can be used to add information to the last_output list
        """
        self.before_execution_functions.append(f)
        return f

    def after_handlers(self, f):
        """Register a function to be called affter all the script handlers.
        Can be used to handle all of the data produced by the scripts
        """
        self.after_handler_functions.append(f)
        return f

    def register_script_handler(self, fn, matcher):
        """Registers a function to be run according to the matcher
        """
        self.script_handlers.append(
            ScriptHandler(matcher, fn, catch_exceptions=not self.debug))
        return fn

    def script_handler(self, matcher):
        """A decorator that is used to register a function for a given
        script::

            @app.script_handler(matchers.Name('users.sh'))
            def handle_users(output):
                print('output')

        :param script_name: the name of the script that triggers the call.
        """
        def decorator(f):
            return self.register_script_handler(f, matcher)
        return decorator

    def script_handler(self, f):
        """Shorthand decorator for adding a script handler with the
        :class:`Any` matcher."""
        return self.register_script_handler(f, matchers.ANY)

    def script_handler_by_name(self, name):
        """Shorthand decorator for handling scripts based on matching a
        regular expression to their filename. Makes use of
        :class:`matcher.Name`

            @app.script_handler_by_name('users.sh')
            def handle_users(output):
                print('output')
        """
        def decorator(f):
            matcher = matchers.Name(name)
            return self.register_script_handler(f, matcher)
        return decorator

    def find_scripts(self):
        """Lists all :class:`Script`s to be executed each step. Their file
        attribute needs to be especified as a correct path, either absolute,
        or relative to the current working directory. Implemented as a
        generator function.
        """
        for name in os.listdir(self.script_dir):
            path = os.path.join(self.script_dir, name)
            if os.path.isfile(path):
                yield self.script_class(name=name, path=path)

    def execute_scripts(self):
        """Runs and reads the result of scripts. """

        def parse_and_append_result(script, output, list_):
            """Parses the output of an script and appends the resulting Result
            object to list_. The Result object will copy the name and path
            attributes from the script parameter.
            """
            try:
                output = output.decode()
                data = json.loads(output)
                result = Result(script, data)
            except ValueError:
                logger.exception('Error parsing output of %s' % script.path)
            else:
                list_.append(result)

        # Setup Timeout
        class TimeoutExpired(Exception):
            pass

        def alarm_handler(signum, frame):
            raise TimeoutExpired

        signal.signal(signal.SIGALRM, alarm_handler)

        # Run scripts.
        scripts = [script for script in self.find_scripts() if
                   script.is_valid()]

        for script in scripts:
            script.run()

        # Read the result of the executed scripts.
        for script in [script for script in scripts if script.ran()]:
            try:
                signal.alarm(self.script_timeout)  # Set alarm.
                out, errs = script.communicate()
                signal.alarm(0)  # Reset alarm.
            except TimeoutExpired:  # Alarm went off.
                logger.warning('Script took too long')
                script.kill()
                out, errs = script.communicate()  # Clear pipes.
            else:
                parse_and_append_result(script, out, self.last_output)

    def run(self):
        """Runs the application's main loop, responsible for executing and
        listening to the scripts
        """
        from .timer import RepeatingTimer
        timer = RepeatingTimer(self.interval)
        timer.register(self.step)
        timer.run()

    def handle_scripts(self):
        """Calls the handler callbacks for each entry in last_output.
        """
        for result in self.last_output:
            for handler in self.script_handlers:
                handler.handle_script(result)

    def step(self):
        """Controls what happens in a iteration.. If the application using
        this library implements its own main loop, you can either run this
        method periodically, or use :method:`run` in its own thread/process.
        """
        self.last_output = []
        self.before_execution_functions()
        self.execute_scripts()
        self.handle_scripts()
        self.after_handler_functions()
