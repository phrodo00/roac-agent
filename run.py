#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import division, print_function, unicode_literals

from roac import Roac

app = Roac(interval=4)

@app.script_handler('uptime.sh')
def handle_uptime(script_name, data):
    print('asdasd')

class Counter(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self.counter=0

    def init_app(self, app):
        self.app = app
        self.app.script_handler('uptime.sh')(self.count)

    def count(self, script_name, data):
        self.counter = self.counter + 1
        print(self.counter)

counter = Counter(app)

app.run()

