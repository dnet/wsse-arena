#!/usr/bin/env python

from __future__ import with_statement
from suds import client
from os import environ
from time import time

before_setup = time()
plugins = []
if 'SIGN' in environ:
	from SudsSigner.plugin import SignerPlugin
	plugins.append(SignerPlugin('../keys/privkey.pem'))

c = client.Client(environ['WSDL_URL'], plugins=plugins)

if 'TIMESTAMP' in environ:
    from suds.wsse import Security, Timestamp
    security = Security()
    security.tokens.append(Timestamp())
    c.set_options(wsse = security)

if 'SECURE' in environ and 'SIGN' not in environ:
    from suds.wsse import Security, UsernameToken
    security = Security()
    token = UsernameToken('admin', 'nimda', 'PLAIN' not in environ)
    security.tokens.append(token)
    c.set_options(wsse = security)

times = int(environ['TIMES']) if 'TIMES' in environ else 1

after_setup = time()

for _ in xrange(times):
	print c.service.say_hello('World', 3)

after_invoke = time()

if 'CSV_FILE' in environ:
    with file(environ['CSV_FILE'], 'a') as f:
        f.write("\r\n{0};{1};{2}".format(environ['CSV_PREFIX'],
            (after_setup - before_setup) * 1000,
            (after_invoke - after_setup) * 1000))
