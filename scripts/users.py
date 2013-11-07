#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
import sys

command = Popen('users', stdout=PIPE, stderr=PIPE)
out, err = command.communicate()
users = list(set(out.split()))
json.dump(users, sys.stdout)
