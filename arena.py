#!/usr/bin/env python

from __future__ import with_statement, print_function
from usage import USAGE, usage_format
from tester import Tester
import json, sys

def main(args):
    with file('arena.json', 'rb') as json_f:
        config = json.load(json_f)
    svc_list = config['services']
    cns_list = config['consumers']
    if len(args) < 2:
        exit_errmsg(USAGE.format(progname=args[0],
			services=usage_format(svc_list),
            consumers=usage_format(cns_list)))
    else:
        tst = Tester()
        if args[1] == 'test':
            svc_name, cns_name = args[2:4]
            tst.test_pair(resolve(svc_list, svc_name, 'service'),
                    resolve(cns_list, cns_name, 'consumer'))
        elif args[1] == 'clean':
            tst.clean(config[args[2] + 's'][args[3]])
        else:
            exit_errmsg('Invalid command: "{0}"'.format(args[1]))

def resolve(options, key, title):
    try:
        return options[key]
    except KeyError:
        exit_errmsg('Invalid {0}: "{1}"'.format(title, key))

def exit_errmsg(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
