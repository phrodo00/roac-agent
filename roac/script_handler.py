# vim: set fileencoding=utf-8 :
from __future__ import absolute_import
import logging


logger = logging.getLogger(__name__)


class ScriptHandler(object):
    def __init__(self, matcher, fn, catch_exceptions=False):
        self.matcher = matcher
        self.fn = fn
        self.catch_exceptions = catch_exceptions

    def handle_script(self, result):
        if self.matcher.match(result):
            try:
                return self.fn(result)
            except Exception:
                logger.debug(self.catch_exceptions)
                if self.catch_exceptions:
                    logger.exception('Error at function: %s' % self.fn)
                else:
                    raise
