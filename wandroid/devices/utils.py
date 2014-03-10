#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
wandroid devices
"""
import pkg_resources
import wandroid.adbw as adbw

def get_devices():
    """
    mainfunc
    """
    entry_points = pkg_resources.iter_entry_points(group='wandroid_devices')
    for ep in entry_points:
        yield ep.name, ep.load()


def list_devices():
    print('installed wandroid.device packages\n'
          '----------------------------------')
    devices = get_devices()
    for name, cls in devices:
        print(name, cls)
    print('')
    print('adb devices\n'
          '-----------')
    adbw.adb('devices')
    print('')


import unittest
class Test_wandroid_devices(unittest.TestCase):
    def test_get_devices(self):
        devices = get_devices()
        devices = list(devices)
        self.assertTrue(bool(len(devices)))


def main():
    import logging
    import optparse
    import os.path
    import sys

    # TODO: argparse
    if '-d' in sys.argv:
        devname = sys.argv[2]
        devices = dict(get_devices())
        if devname not in devices:
            raise Exception("%r not in %r" % (devname, devices.keys()))
        cls = devices.get(devname)
        scriptname = os.path.basename(cls.__module__)
        newargs = [scriptname] + sys.argv[3:]
        print(newargs)
        return cls.main(*newargs)

    prs = optparse.OptionParser(usage="%prog : args")

    prs.add_option('-l', '--list-devices',
                    dest='list_devices',
                    action='store_true',
                    help='List supported devices')

    prs.add_option('-v', '--verbose',
                    dest='verbose',
                    action='store_true',)
    prs.add_option('-q', '--quiet',
                    dest='quiet',
                    action='store_true',)
    prs.add_option('-t', '--test',
                    dest='run_tests',
                    action='store_true',)

    (opts, args) = prs.parse_args()

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    if opts.run_tests:
        sys.argv = [sys.argv[0]] + args
        import unittest
        sys.exit(unittest.main())

    if opts.list_devices:
        list_devices()



if __name__ == "__main__":
    import sys
    sys.exit(main())
