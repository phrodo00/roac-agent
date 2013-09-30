# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
from subprocess import Popen, PIPE
from collections import namedtuple
from . import matchers
from .functionlist import FunctionList
from .config import Config, ConfigAttribute
import sys
import os
import subprocess
import json
import time
import signal


Script = namedtuple('Script', ['name', 'file'])


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
    script_dir  = ConfigAttribute('script_dir')
    debug = ConfigAttribute('debug')
    script_timeout = ConfigAttribute('script_timeout')

    def __init__(self, **kwargs):
        self.config = Config(self.default_config)
        self.config.update(kwargs)
        self.script_handlers = []
        self.before_execution_functions = FunctionList()
        self.after_handler_functions = FunctionList()

    def before_excecution(self, f):
        self.before_execution_functions.append(f)
        return f

    def after_handlers(self, f):
        self.after_handler_functions.append(f)
        return f

    def register_script_handler(self, fn, matcher):
        self.script_handlers.append((matcher, fn))
        return fn

    def script_handler(self, matcher):
        """A decorator that is used to register a view function for a given
        script::

            @app.script_handler('users.sh')
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
        for root, dirs, files in os.walk(self.script_dir):
            for name in files:
                yield Script(name=name, file=os.path.join(root, name))

    def valid_script(self, script):
        """Checks whether to run a script. Right now we only check whether it
        is writtable by others for security.
        """
        stat = os.stat(script.file)
        can_be_written_by_others = bool(stat.st_mode & 0002)
        return not can_be_written_by_others

    def execute_scripts(self):
        """Runs and reads the result of scripts. """

        class TimeoutExpired(Exception):
            pass

        def alarm_handler(signum, frame):
            raise TimeoutExpired

        signal.signal(signal.SIGALRM, alarm_handler)

        for script in self.find_scripts():
            if not self.valid_script(script):
                continue  # Don't attempt to run script if invalid.
            try:
                print('Executing {}'.format(script.name))
                signal.alarm(self.script_timeout)
                proc = Popen(script.file, stdout=PIPE)
                out, errs = proc.communicate()
                signal.alarm(0)  # Reset the alarm
                out = out.decode()
                data = json.loads(out)
            except (OSError, ValueError) as e:
                print('\terror: {}'.format(e))
            except TimeoutExpired:
                print('Script took too long')
                proc.kill()
                proc.communicate()
            else:
                #Call functions binded to this script
                self.last_output[script.name] = data

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
        for script_name, data in self.last_output.iteritems():
            for handler in self.script_handlers:
                # Probably should change handler to an object or named tuple
                if handler[0].match(script_name, data):
                    try:
                        handler[1](script_name, data)
                    except Exception as e:
                        if(self.debug):
                            raise
                        else:
                            print('Error at function: {}'.format(e))

    def step(self):
        """Controls what happens in a iteration.. If the application using
        this library implements its own main loop, you can either run this
        method periodically, or use :method:`run` in its own thread/process.
        """
        self.last_output = {}
        self.before_execution_functions()
        self.execute_scripts()
        self.handle_scripts()
        self.after_handler_functions()
