#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import print_function
import pprint
import logging
from roac import Roac, Result, matchers, logs
from roac.ext.http_poster import HTTPPoster

app = Roac()

app.config.from_file('run.json')
logs.log_to_stderr()  # Log to stderr even outside debug mode


@app.script_handler_by_name('^uptime.sh$')
def handle_uptime(result):
    print('Uptime Handler')


class Counter(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self.counter = 0

    def init_app(self, app):
        self.app = app
        self.app.register_script_handler(
            self.count, matchers.And(matchers.Name('sh$'), matchers.ANY))

    def count(self, result):
        self.counter = self.counter + 1
        logging.info(self.counter)

counter = Counter(app)


@app.after_handlers
def print_output():
    print('-----------------------------------------------------------------')
    for result in app.last_output:
        print('Script: %s' % result.name)
        pprint.pprint(result.data)
    print('-----------------------------------------------------------------')


#@app.script_handler_by_name('sh$')
def fail(result):
    raise Exception(script_name)


@app.script_handler
def any(result):
    logging.info('ANY handler')


poster = HTTPPoster(app)

app.run()
