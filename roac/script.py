# vim: set fileencoding=utf-8 :

from . import Result
from subprocess import Popen, PIPE
import logging
import json


logger = logging.getLogger(__name__)


def parse_and_append_result(script, output, list_):
    """Parses the output of an script and appends the resulting Result object
    to list_. The Result object will copy the name and path attributes from
    the script parameter.
    """
    try:
        output = output.decode()
        data = json.loads(output)
        result = Result(script, data)
    except ValueError:
        logger.exception('Error parsing output of %s' % script.path)
    else:
        list_.append(result)


class Script(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.popen = None

    def run(self):
        """Starts runnnig the script"""
        logger.debug('Running script %s', self.path)
        try:
            self.popen = Popen(self.path, stdout=PIPE)
        except OSError as e:
            logger.exception('Error running %s' % self.path)
            self.popen = None
        return self.popen

    def ran(self):
        """Indicates whether the script has ran succesfully"""
        return self.popen is not None

    def communicate(self, *args, **kwargs):
        """Calls communicate on the Popen object. For more info see the
        subprocess documentation
        """
        if self.popen:
            logger.debug('Reading output of %s', self.path)
            self.out, self.err = self.popen.communicate(*args, **kwargs)
            return (self.out, self.err)

    def kill(self, *args, **kwargs):
        """Calls kill on the Popen object. For more info see the subprocess
        documentation
        """
        if self.popen:
            logger.debug('Killing script %s', self.path)
            return self.popen.kill(*args, **kwargs)
