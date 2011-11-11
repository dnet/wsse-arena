#!/usr/bin/env python

from suds import client
from os import environ

c = client.Client(environ['WSDL_URL'])

if 'SECURE' in environ:
    from suds.wsse import Security, UsernameToken
    security = Security()
    token = UsernameToken('admin', 'nimda', 'PLAIN' not in environ)
    security.tokens.append(token)
    c.set_options(wsse = security)

print c.service.say_hello('World', 3)
