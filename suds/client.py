#!/usr/bin/env python

from suds import client
from os import environ

plugins = []
if 'SIGN' in environ:
	from SudsSigner.plugin import SignerPlugin
	plugins.append(SignerPlugin('../keys/privkey.pem'))

c = client.Client(environ['WSDL_URL'], plugins=plugins)

if 'SECURE' in environ and 'SIGN' not in environ:
    from suds.wsse import Security, UsernameToken
    security = Security()
    token = UsernameToken('admin', 'nimda', 'PLAIN' not in environ)
    security.tokens.append(token)
    c.set_options(wsse = security)

print c.service.say_hello('World', 3)
