#!/usr/bin/env python

from suds import client
from os import environ

c = client.Client(environ['WSDL_URL'])
print c.service.say_hello('World', 3)
