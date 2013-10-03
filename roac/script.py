# vim: set fileencoding=utf-8 :

from subprocess import Popen, PIPE
import logging


logger = logging.getLogger(__name__)


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
