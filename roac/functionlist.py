# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
import logging


class FunctionList(list):
    """Allows calling a list of functions at the same time with the same
    arguments.
    """
    def call(self, *args, **kwargs):
        return [fn(*args, **kwargs) for fn in self]
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
