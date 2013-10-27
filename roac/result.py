# vim: set fileencoding=utf-8 :
from __future__ import absolute_import


class Result(object):
    """Holds the result of an script. Used to interface with script handlers
    and matchers
    """
    def __init__(self, script, data):
        self.name = script.name
        self.path = script.path
        self.data = data
