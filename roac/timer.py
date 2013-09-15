# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
from collections import namedtuple
import time


Callback = namedtuple('Callback', ['function', 'args', 'kwargs'])


class RepeatingTimer:
    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []

    def register(self, f, *args, **kwargs):
        self.callbacks.append(Callback(f, args, kwargs))

    def run(self):
        while True:
            now = time.time()
            for callback in self.callbacks:
                callback.function(*callback.args, **callback.kwargs)
            time.sleep(self.interval - (time.time() - now))
