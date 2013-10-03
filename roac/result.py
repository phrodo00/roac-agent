# vim: set fileencoding=utf-8 :
import json
import logging


logger = logging.getLogger(__name__)


def append_result(script, output, list_):
    try:
        result = Result(script, output)
    except ValueError:
        logger.exception('Error reading output of %s' % script.path)
    else:
        list_.append(result)


class Result(object):
    """Parses the output of an script"""
    def __init__(self, script, output):
        self.name = script.name
        self.path = script.path
        output = output.decode()
        self.data = json.loads(output)
