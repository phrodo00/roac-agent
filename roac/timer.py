# vim: set fileencoding=utf-8 :
from __future__ import absolute_import
from collections import namedtuple
import time
import logging


Callback = namedtuple('Callback', ['function', 'args', 'kwargs'])
logger = logging.getLogger(__name__)


class RepeatingTimer:
    """Calls a set of functions in regular intervals"""

    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []

    def register(self, f, *args, **kwargs):
        """Adds a function to be called each interval"""
        self.callbacks.append(Callback(f, args, kwargs))

    def run(self):
        """Gets the timer running"""
        self.running = True
        while self.running:
            start_iter = time.time()
            for callback in self.callbacks:
                callback.function(*callback.args, **callback.kwargs)
            sleep_time = self.interval - (time.time() - start_iter)
            if(sleep_time > 0):
                time.sleep(sleep_time)
            else:
                logger.warning('Iteration took too long')
