# vim: set fileencoding=utf-8 :

from subprocess import Popen, PIPE
import logging


logger = logging.getLogger(__name__)


class Script(object):
    
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def run(self):
        logger.debug('Running script %s', self.path)
        try:
            self.popen = Popen(self.path, stdout=PIPE)
        except OSError as e:
            logger.exception('Error running %s' % self.path)
            self.popen = None
        return self.popen

    def ran(self):
        return self.popen is not None

    def communicate(self, *args, **kwargs):
        if self.popen:
            logger.debug('Reading output of %s', self.path)
            self.out, self.err = self.popen.communicate(*args, **kwargs)
            return (self.out, self.err)
        else:
            return None
        
    def kill(self, *args, **kwargs):
        if self.popen:
            logger.debug('Killing script %s', self.path)
            return self.popen.kill(*args, **kwargs)
        else:
            return None
