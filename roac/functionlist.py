# vim: set fileencoding=utf-8 :
import logging


logger = logging.getLogger(__name__)


class FunctionList(list):
    """Allows calling a list of functions at the same time with the same
    arguments.
    """
    def __init__(self, iterable, catch_exceptions=False):
        list.__init__(self, iterable)
        self.catch_exceptions = catch_exceptions

    def __init__(self, catch_exceptions=False):
        list.__init__(self)
        self.catch_exceptions = catch_exceptions

    def call(self, *args, **kwargs):
        rvs = []
        for fn in self:
            try:
                rvs.append(fn(*args, **kwargs))
            except Exception:
                if self.catch_exceptions:
                    logger.exception('Error calling %s' % fn)
                else:
                    raise
        return rvs

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)
