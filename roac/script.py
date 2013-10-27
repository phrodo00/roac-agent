# vim: set fileencoding=utf-8 :
from __future__ import absolute_import

from subprocess import Popen, PIPE
import logging
import os


logger = logging.getLogger(__name__)


class Script(object):

    def __init__(self, name, path):
        # Identifier for the script. Usually the file name, but doesn't need
        # to be
        self.name = name
        # path of the actual script file, either absolute or relative to CWD
        self.path = path
        # Placeholder for subprocess object.
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

    def is_valid(self):
        """Checks whether to run a script. Right now we only check whether it
        is writtable by others for security.
        """
        stat = os.stat(self.path)
        can_be_written_by_others = bool(stat.st_mode & 0002)
        return not can_be_written_by_others
