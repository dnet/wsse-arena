#!/usr/bin/env python

from __future__ import division
from itertools import imap
from socket_tools import get_free_portnum, get_listener
from subprocess import Popen, PIPE
import os, time, sys

HOST = 'localhost'
TIMEOUT_MS = 10000
CUR_DIR = os.getcwd()

class Tester(object):
    def __init__(self):
        self.port = get_free_portnum(HOST)
        self.endpoint_url = 'http://{host}:{port}/test'.format(
                host=HOST, port=self.port)
        self.env = dict(os.environ)
        self.env['ENDPOINT_URL'] = self.endpoint_url
        self.listener = get_listener()
        self.env['CONNECT_BACK'] = ':'.join(imap(str, self.listener.getsockname()))

    def extend_env(self, value):
        self.env.update(value)

    def clean(self, subject):
        if 'cleancmd' in subject:
            self.start(subject, 'clean').wait()

    def test_pair(self, service, consumer):
        self.env['WSDL_URL'] = service['wsdl'].format(
                endpoint_url=self.endpoint_url)
        svc_proc = self.start(service)
        try:
            self.ensure_listener(service, svc_proc)
            cns_proc = self.start(consumer, stdout=PIPE)
            stdout, _ = cns_proc.communicate()
            if consumer['expected'] not in stdout:
                raise RuntimeError('Unexpected output: "{0}"'.format(stdout))
        finally:
            svc_proc.terminate()
            svc_proc.wait()

    def start(self, subject, cmd='start', stdout=None):
        cwd = get_subject_dir(subject)
        return Popen([subject[cmd + 'cmd']], shell=True, cwd=cwd,
                env=self.env, stdout=stdout)

    def ensure_listener(self, service, process):
        self.listener.settimeout(TIMEOUT_MS / 1000)
        connection, _ = self.listener.accept()
        connection.close()
        time.sleep(1)


def get_subject_dir(subject):
    return os.path.join(CUR_DIR, subject['directory'])
