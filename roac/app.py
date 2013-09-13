# vim: encoding: utf-8
from __future__ import division, print_function, unicode_literals
from subprocess import Popen, PIPE
import sys
import os
import subprocess
import json
import time


DEFAULT_CONFIG = {
    'script_dir': 'scripts',
    'delay': 30
    }


class Roac(object):

    def __init__(self, **kwargs):
        self.config = DEFAULT_CONFIG
        self.config.update(kwargs)

    def execute_scripts(self):
        for root, dirs, files in os.walk(self.config['script_dir']):
            for name in files:
                try:
                    print('Executing {}'.format(name))
                    process = Popen(os.path.join(root, name), stdout=PIPE)
                    # regression: python2's subprocess doesn't support timeout
                    # deal with it manually later.
                    # see http://stackoverflow.com/questions/1191374
                    out, errs = process.communicate()
                    out = out.decode()
                    print(out)
                    data = json.loads(out)
                    print(data)
                except (OSError, ValueError) as e:
                    print('\terror: {}'.format(e))

    def run(self):
        while True:
            now = time.time()
            self.execute_scripts()
            time.sleep(self.config['delay'] - (time.time() - now))
