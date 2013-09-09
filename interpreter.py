#!/usr/bin/python

from subprocess import Popen, PIPE
import sys, os
import subprocess, json
import time

def execute_scripts():
    for root, dirs, files in os.walk('scripts'): #parametrize in config file
        for name in files:
            try:
                print('Executing {}'.format(name))
                process = Popen(os.path.join(root, name), stdout=PIPE)
                out, errs = process.communicate(timeout=10)
                out = out.decode()
                print(out)
                data = json.loads(out)
                print(data)
            except (OSError, ValueError) as e:
                print('\terror: {}'.format(e))
            except subprocess.TimeoutExpired:
                proc.kill()
                out, errs = proc.communicate() #clear pipes.
                print('Script took too long')

def main(argv):
    delay = 5
    while True:
        now = time.time()
        execute_scripts()
        time.sleep(delay - (time.time() - now))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

