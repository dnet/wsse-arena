#!/usr/bin/env python

from itertools import imap
from os import linesep

USAGE = """Usage:
\tPair test: {progname} test <service> <consumer>
\tClean:     {progname} clean [service|consumer] <name>
\tMeasure:   {progname} measure [suite] [repeats] [runs]

Available service(s):
{services}

Available consumer(s):
{consumers}

Available suite(s):
{suites}
"""

def usage_format(options):
    space = str(max(imap(unicode.__len__, options.iterkeys())) + 2)
    lines = (('\t{0:' + space + '} -- {1}').format(key, value['title'])
            for key, value in options.iteritems())
    return linesep.join(lines)
