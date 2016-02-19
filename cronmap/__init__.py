import sys
import time
import datetime
import subprocess


class Cronmap(object):
    def __init__(self, args):
        self.ips = args.ips
        if args.nmap_args:
            self.nmap_args = [a[0] for a in args.nmap_args]
        else:
            self.nmap_args = ['-sV', '-Pn', '-p0-65535']
        self.delay = args.delay
        self.outfile = args.outfile
        self.email = args.email
        self.debug = args.debug

    def _run_scan(self):
        if self.debug:
            print "Invoking nmap " + ' '.join(self.nmap_args) + ' ' +\
                ' '.join(self.ips)
        return subprocess.check_output(["nmap"] + self.nmap_args + self.ips)

    def run(self):
        while True:
            try:
                if self.debug:
                    print "Running scan", datetime.datetime.now()
                nmap_out = self._run_scan()

                if self.outfile != sys.stdout:
                    if self.debug:
                        print nmap_out

                self.outfile.write(nmap_out)
                self.outfile.flush()
                time.sleep(self.delay)
            except KeyboardInterrupt:
                if self.outfile is not sys.stdout:
                    self.outfile.close()
                return
