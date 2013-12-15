#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
chrome
"""

import wandroid.adbw as adbw

def get_bookmarks():
    files = (
        '/data/data/com.android.chrome/app_chrome/Default/Bookmarks',
        '/data/data/com.android.chrome/app_chrome/Default/Bookmarks.bak')
    retrieved = []
    for f in files:
        retrieved.append(adbw.get_remote_file(f))
    return retrieved


def get_history():
    files = (
        '/data/data/com.android.chrome/app_chrome/Default/History',
        '/data/data/com.android.chrome/app_chrome/Default/History-journal')
    retrieved = []
    for f in files:
        retrieved.append(adbw.get_remote_file(f))
    return retrieved



def chrome():
    """
    mainfunc
    """
    pass


import unittest
class Test_chrome(unittest.TestCase):
    def test_chrome(self):
        pass


def main():
    import optparse
    import logging

    prs = optparse.OptionParser(usage="./%prog : args")

    prs.add_option('-B', '--bookmarks',
                    dest='get_bookmarks',
                    action='store_true',
                    help='Retrieve bookmarks from device')
    prs.add_option('-H', '--history',
                    dest='get_history',
                    action='store_true',
                    help='Retrieve history from device')

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
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        exit(unittest.main())

    if opts.get_bookmarks:
        get_bookmarks()

    if opts.get_history:
        get_history()


if __name__ == "__main__":
    main()
