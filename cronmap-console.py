#!/usr/bin/env python

from __future__ import absolute_import

import sys
import argparse

from cronmap.console import ConsoleMap, Options, palettes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cronmap: scan a set of IPs'
                                                 'on a set schedule')
    parser.add_argument('-d', dest='debug', action='store_const', const=True,
                        default=False, help='enable debug output to stdout')
    parser.add_argument(
        "--palette", type=str, default=palettes.DEFAULT,
        action="store", dest="palette",
        choices=sorted(palettes.palettes.keys()),
        help="Select color palette: " + ", ".join(palettes.palettes.keys())
    )
    args = parser.parse_args()

    if args.debug:
        print repr(args)

    o = Options(debug=args.debug, palette=args.palette)
    cm = ConsoleMap(o)
    cm.run()
