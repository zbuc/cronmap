from __future__ import absolute_import

import sys
import time
import datetime
import subprocess


class Cronmap(object):
    def __init__(self, options):
        # self.ips = args.ips
        # if args.nmap_args:
        #     self.nmap_args = [a[0] for a in args.nmap_args]
        # else:
        #     self.nmap_args = ['-sV', '-Pn', '-p0-65535']
        # self.delay = args.delay
        # self.outfile = args.outfile
        # self.email = args.email
        self.options = options

    def _run_scan(self):
        if self.debug:
            print "Invoking nmap " + ' '.join(self.nmap_args) + ' ' +\
                ' '.join(self.ips)
        return subprocess.check_output(["nmap"] + self.nmap_args + self.ips)
