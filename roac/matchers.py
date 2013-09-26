# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
import re

"""Collection of matchers for use in :class:`Roac`. They control when handler
functions should be called"""


class ProtoMatcher(object):
    """Example of a matcher, doesn't match anything"""
    def match(self, script_name, data):
        """If this method returns True, then the handler function associated
        to this matcher is run"""
        return False


class MatchAnything(object):
    """Will call function for each script"""
    def match(self, script_name, data):
        return True


class MatchName(object):
    def __init__(self, pattern):
        self.prog = re.compile(pattern)

    def match(self, script_name, data):
        return self.prog.search(script_name) is not None
