#!/usr/bin/env python

import sys
import argparse

from cronmap import Cronmap


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cronmap: scan a set of IPs'
                                                 'on a set schedule')
    parser.add_argument('ips', metavar='ip', type=str, nargs='+',
                        help='IPs to be scanned')
    parser.add_argument('--nmap-args', type=str, help='arguments to pass to '
                        'nmap, default -sV -Pn -p0-65535', nargs='*',
                        action='append',
                        dest='nmap_args')
    parser.add_argument('--delay', type=int, help='delay in seconds between '
                        'scans, default 21600 seconds/6 hours', default=21600)
    parser.add_argument('--outfile', type=argparse.FileType('a'),
                        default=sys.stdout, help='file to log results to, '
                        'default stdout')
    parser.add_argument('-d', dest='debug', action='store_const', const=True,
                        default=False, help='enable debug output to stdout')
    parser.add_argument('--email', type=str, help='destination address for '
                        'emailed results')
    args = parser.parse_args()

    if args.debug:
        print repr(args)

    cm = Cronmap(args)
    cm.run()
