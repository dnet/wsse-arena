#!/usr/bin/env python

import socket

def get_listener():
	sock = socket.socket()
	sock.bind(('127.0.0.1', 0))
	sock.listen(1)
	return sock

def get_free_portnum(host):
    sock = socket.socket()
    sock.bind((host, 0))
    _, port = sock.getsockname()
    sock.close()
    return port
