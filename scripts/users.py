#!/usr/bin/env python

from subprocess import check_output
import json
import sys

users = check_output('users')
users = list(set(users.split()))
json.dump(users, sys.stdout)
