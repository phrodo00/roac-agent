#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import division, print_function, unicode_literals
import pprint
from roac import Roac, matchers

app = Roac(interval=4, script_timeout=1)


@app.script_handler_by_name('^uptime.sh$')
def handle_uptime(script_name, data):
    print('Uptime Handler')


class Counter(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self.counter = 0

    def init_app(self, app):
        self.app = app
        self.app.register_script_handler(self.count, 
                matchers.And(matchers.Name('sh$'), matchers.Any()))

    def count(self, script_name, data):
        self.counter = self.counter + 1
        print(self.counter)

counter = Counter(app)


@app.after_handlers
def after():
    pprint.pprint(app.last_output)

@app.script_handler_by_name('sh$')
def raises(script_name, data):
    raise Exception(script_name)

app.run()
