#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import print_function
import pprint
import logging
from roac import Roac, matchers, logs

app = Roac()

app.config.from_file('run.json')
logs.log_to_stderr()  # Log to stderr even outside debug mode


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
                matchers.And(matchers.Name('sh$'), matchers.ANY))

    def count(self, script_name, data):
        self.counter = self.counter + 1
        logging.info(self.counter)

counter = Counter(app)


@app.after_handlers
def after():
    pprint.pprint(app.last_output)

@app.script_handler_by_name('sh$')
def fails(script_name, data):
    raise Exception(script_name)

@app.script_handler
def any(script_name, data):
    logging.info('ANY handler')

import requests
import socket
import json

class AggregatorPoster(object):
    """Posts the scripts' data to an aggregator"""
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self.node_name = socket.gethostname()

    def init_app(self, app):
        self.app = app
        app.after_handlers(self.post_to_service)

    def post_to_service(self):
        url_template = app.config['aggregator_url']
        url = url_template.format(node_name=self.node_name)
        logging.info(url)
        r = requests.post(url, data=json.dumps(app.last_output),
                          headers={'Content-Type': 'application/json'})

poster = AggregatorPoster(app)

app.run()
