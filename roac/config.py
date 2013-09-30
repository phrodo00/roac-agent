# vim: set fileencoding=utf-8 :
from __future__ import division, print_function, unicode_literals
import json
import os


class ConfigAttribute(object):
    """Descriptor that redirects itself to a dictionary key in the config
    attribute of an object
    """
    def __init__(self, key):
        self.__name__ = key

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.config[self.__name__]

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    """Handles app configuration. Also provides methods for loading 
    configuration values from files
    """

    def __init__(self, default=None):
        if default is None:
            default = {}
        dict.__init__(self, default)

    def from_json(self, s):
        """Reads a json-formated string and loads it as configuration values.
        The top parent needs to be an object or it raises TypeError.
        """
        data = json.loads(s)
        self.update(data)

    def from_file(self, name):
        """Reads a json-formated file and loads it as configuration values.
        The top parent needs to be an object or it raises TypeError.
        """
        with open(name) as f:
            data = json.load(f)
            self.update(data)

    def from_envvar(self, envvar):
        """Reads a json-formated file pointed by the environment variable 
        envvar and loads it as configuration values.
        The top parent needs to be an object or it raises TypeError.
        """
        if envvar in os.environ:
            name = os.environ[envvar]
            self.from_file(name)
