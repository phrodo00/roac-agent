#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import division, print_function, unicode_literals

from roac import Roac

app = Roac(interval=4)

@app.script_handler('uptime.sh')
def handle_uptime(output):
    print('asdasd')

app.run()

