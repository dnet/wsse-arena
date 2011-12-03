#!/usr/bin/env python

from __future__ import with_statement
from itertools import product
from tester import Tester
from datetime import datetime
from os import getcwd, path

FILE_FORMAT = 'arena-measurement-%Y%m%d-%H%M%S'
LOG_SUFFIX = '.log'
CSV_SUFFIX = '.csv'

def measure(suites, repeats, runs, svc_list, cns_list):
    filebase = datetime.now().strftime(FILE_FORMAT)
    log = LogFile(filebase)
    csv = path.join(getcwd(), filebase + CSV_SUFFIX)
    with file(csv, 'w') as f:
        f.write('Service;Consumer;Repeats;Suite;Initialization;Invocation')
    for suite, repeat, (svc_name, service), (cns_name, consumer), num in product(
            suites, repeats, svc_list.iteritems(), cns_list.iteritems(), xrange(runs)):
        log.log('{0} using {1} -({2}x)-> {3}, try {4}'.format(
            suite['title'], cns_name, repeat, svc_name, num + 1))
        tst = Tester()
        env = dict(TIMES=str(repeat), CSV_FILE=csv, CSV_PREFIX=';'.join(
            (svc_name, cns_name, str(repeat), suite['title'])))
        for i in suite['env']:
            env[i] = '1'
        tst.extend_env(env)
        tst.test_pair(service, consumer)

class LogFile(object):
    def __init__(self, filebase):
        self.logfile = filebase + LOG_SUFFIX

    def log(self, txt):
        with file(self.logfile, 'a') as f:
            f.write(datetime.now().isoformat())
            f.write(' ')
            f.write(txt)
            f.write("\n")
