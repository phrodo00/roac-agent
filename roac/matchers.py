# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
import re

"""Collection of matchers for use in :class:`Roac`. They control when handler
functions should be called"""


class Nothing(object):
    """Example of a matcher, doesn't match anything"""
    def match(self, script_name, data):
        """If this method returns True, then the handler function associated
        to this matcher is run"""
        return False


class Any(object):
    """Will call function for each script"""
    def match(self, script_name, data):
        return True


class And(object):
    """Combines multiple matches in an and statement.
    (to do an or, simply register a single function multiple times with
    different matchers
    """
    def __init__(self, *args):
        self.matchers = args

    def match(self, script_name, data):
        results = [matcher.match(script_name, data)
                   for matcher in self.matchers]
        return reduce(lambda x, y: x and y, results)


class Name(object):
    """Matches the script name to the regular expression pattern it's
    initialized with
    """
    def __init__(self, pattern):
        self.prog = re.compile(pattern)

    def match(self, script_name, data):
        return self.prog.search(script_name) is not None
