#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
adbw(rapper)
============
A wrapper for common adb functions


requirements
-------------
sh -- sane subprocess wrapper that raises Exceptions when $? != 0

"""
import functools

import sh
sh.logging_enabled = True

ADB_COMMAND = 'adb'
adb = sh.Command(ADB_COMMAND)

adbsh = functools.partial(adb, 'shell')
adbsu = functools.partial(adb, 'shell', 'su', '-c')

def to_flat_path(path):
    _path = path.replace('/', ',')
    return _path

def to_sd_path(path):
    sdpath = "/sdcard/%s" % to_flat_path(path)
    return sdpath


def get_remote_file(path, dest=None, backup=True):
    sdpath = to_sd_path(path)
    sdbackuppath = "%s.backup" % sdpath
    if dest is None:
        dest = to_flat_path(path)

    adbsu('cp', path, sdpath)
    if backup:
        adbsh('cp', sdpath, sdbackuppath)
    adb('pull', sdpath, dest)
    return dest


def push_remote_file(source, dest):
    sdpath = to_sd_path(dest)
    adb('push', source, sdpath)
    adbsu('cp', sdpath, dest)
    return dest


def update_remote_file(path, func, show_diff=False):
    localpath = get_remote_file(path)
    localbackuppath = "%s.backup" % localpath
    sh.cp(localpath, localbackuppath)

    func(localpath)

    if show_diff:
        p = sh.diff('-Nau', localpath, localbackuppath, _ok_code=[0,1])
        print(p.stdout)

    push_remote_file(localpath, path)


def remount_rw(path):
    return adbsu('mount -o remount,rw', path)


import unittest
class Test_update_remote_file(unittest.TestCase):
    def test_update_remote_file(self):
        pass


def main():
    import optparse
    import logging

    prs = optparse.OptionParser(usage="./%prog : args")

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

    update_remote_file()

if __name__ == "__main__":
    main()

