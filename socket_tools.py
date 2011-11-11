#!/usr/bin/env python

from __future__ import division
import socket, time

def ensure_listener(host, port, timeout):
    start = time.time()
    while time.time() < start + timeout / 1000:
        sock = socket.socket()
        try:
            sock.connect((host, port))
        except socket.error:
            time.sleep(0.01)
        else:
            return
        finally:
            sock.close()
    raise RuntimeError('Listener timeout')

def get_free_portnum(host):
    sock = socket.socket()
    sock.bind((host, 0))
    _, port = sock.getsockname()
    sock.close()
    return port
