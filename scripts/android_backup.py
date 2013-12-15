#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
android_backup -- an adb wrapper

why?
----
* sometimes it's not helpful to restore/overwrite different components
* AFAIK there's no easy way to split an existing .ab
* because i'll never remember which file is which
* because i want a flat directory of standard, dated backups

.. note::

        $ adb backup -all -system -apk
        Now unlock your device and confirm the backup operation.

        [hangs]

"""
import collections
import datetime
import logging
import os
import subprocess

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def get_backup_sets(path=None, generate_filename=True, include_date=True):
    backups = collections.OrderedDict((
        ('default', {
            'name': 'default',
            'all': True,
            'apk': True,
            #'obb': False,
            #'shared': False,
            'system': True,
            'path': path,
            'generate_filename': generate_filename,
            'include_date': include_date}),
        #('everything',{
            #'name': 'everything',
            #'all': True,
            #'apk': True,
            #'system': True,
            #'obb': True,
            ##'shared': True,
            #'path': path,
            #'generate_filename': generate_filename,
            #'include_date': include_date}),
        #('system', {
            #'name': 'system',
            #'system': True,
            #'obb':True,
            #'apk': True,
            #'all': True, # TODO ?
            #'shared': False,
            #'path': path,
            #'generate_filename': generate_filename,
            #'include_date': include_date}),
        #('myapps', {
            #'name': 'myapps',
            #'system': False,
            #'obb': True,
            #'apk': True,
            ##'shared': True,
            #'path': path,
            #'generate_filename': generate_filename,
            #'include_date': include_date}),
        #('shared', {
            #'name': 'shared',
            #'shared': True,
            #'generate_filename': generate_filename,
            #'include_date': include_date}),
    ))
    return backups


# see: `adb -help 2>&1 | grep 'adb backup' -A 19`
DEFAULT_OPTS = collections.OrderedDict((
    ('apk', False),
    ('obb', False),
    ('shared', False),
    ('system', False),
))
def adb_backup_cmd(
        path=None,
        allpackages=False,
        packages=None,
        generate_filename=False,
        include_date=True,
        name=None,
        adbcmd='adb',
        **kwargs):

    _opts = DEFAULT_OPTS.copy()
    _opts.update(**kwargs)

    if _opts.get('all') == True:
        allpackages = True

    if generate_filename:
        _name = ['backup-']
        if include_date:
            if isinstance(include_date, datetime.datetime):
                date = include_date
            else:
                date = datetime.datetime.now()
            _name.append(date.strftime('%Y%m%d-%H%M'))
        if name:
            _name.append(name)

        for opt in DEFAULT_OPTS:
            value = _opts.get(opt, None)
            if value is True:
                _name.append('%s' % opt)
            elif value is False:
                _name.append('no%s' % opt)
        if allpackages:
            _name.append('all')
        if packages:
            _name.append('-')
            _name.extend(packages)
        filename = u'%s.ab' % str.join('-', _name)
        if path:
            path = os.path.join(path, filename)
        else:
            path = filename

    cmd = [adbcmd, 'backup']

    if path is None:
        path = 'backup.ab'
    cmd.extend(['-f', path])

    for opt in DEFAULT_OPTS:
        value = _opts.get(opt, None)
        if value is True:
            cmd.append('-%s' % opt)
        elif value is False:
            cmd.append('-no%s' % opt)
    if allpackages:
        cmd.append('-all')
        if packages:
            raise Exception('specified packages and -all')
    else:
        if packages:
            cmd.extend(packages)
    return cmd, path


def android_backup(path=None, backup_sets=None, include_date=True):
    """
    Do backups for the specified backup sets
    """
    if not os.path.exists(path) and os.path.isdir(path):
        log.debug("creating directory: %r" % path)
        os.makedirs(path)
    ALL_BACKUP_SETS = get_backup_sets(path=path, include_date=include_date)
    configs = ALL_BACKUP_SETS.keys()
    if backup_sets:
        configs = [name for name in configs if name in backup_sets]
    for set_name in configs:
        kwargs = ALL_BACKUP_SETS.get(set_name)
        cmd, filepath = adb_backup_cmd(**kwargs)
        log.info('## %r: %r' % (set_name, cmd))
        retcode = subprocess.call(cmd)
        if retcode != 0:
            log.error(retcode)
            raise Exception('%r returned %d' % (cmd, retcode))
        log.info('# %r complete' % set_name)


import unittest
class Test_android_backup(unittest.TestCase):
    def setUp(self):
        self.testdate = datetime.datetime(2013, 12, 04, 01, 01)
        self.testdatestr = '20131204-0101'

    def test_adb_backup_cmd(self):
        testdate, testdatestr = self.testdate, self.testdatestr
        testdata = (
            ({'apk': True, 'obb': True, 'shared': True, 'system':True},
             (['adb', 'backup',
               '-f', 'backup.ab',
               '-apk',
               '-obb',
               '-shared',
               '-system'],
              'backup.ab')),
            ({'all': True},
             (['adb', 'backup',
               '-f', 'backup.ab',
               '-noapk',
               '-noobb',
               '-noshared',
               '-nosystem',
               '-all'],
              'backup.ab')),
            ({'apk': False, 'all': True},
             (['adb', 'backup',
               '-f', 'backup.ab',
               '-noapk',
               '-noobb',
               '-noshared',
               '-nosystem',
               '-all'],
              'backup.ab')),
            ({'packages':['one','two']},
             (['adb', 'backup',
               '-f', 'backup.ab',
               '-noapk',
               '-noobb',
               '-noshared',
               '-nosystem',
               'one', 'two'],
              'backup.ab')),
            ({'generate_filename': True,
              'path': '/tmp',
              'include_date': testdate},
             (['adb', 'backup',
               '-f', '/tmp/backup--%s-noapk-noobb-noshared-nosystem.ab' % testdatestr,
               '-noapk',
               '-noobb',
               '-noshared',
               '-nosystem',
               ],
              '/tmp/backup--%s-noapk-noobb-noshared-nosystem.ab' % testdatestr)),
            ({'generate_filename': True,
              'apk': True,
              'system': True,
              'shared': False,
              'include_date': testdate,
              'path':'/tmp'},
             (['adb', 'backup', '-f',
              '/tmp/backup--%s-apk-noobb-noshared-system.ab' % testdatestr,
              '-apk',
              '-noobb',
              '-noshared',
              '-system',
              ],
             u'/tmp/backup--20131204-0101-apk-noobb-noshared-system.ab'))
        )
        for i, o in testdata:
            output = adb_backup_cmd(**i)
            try:
                self.assertEqual(output, o)
            except:
                print(i)
                print(o)
                print(output)
                raise

    #def test_android_backup(self):
    #    testdate, testdatestr = self.testdate, self.testdatestr
    #    android_backup(include_date=self.testdate)


def main(*args):
    import logging
    import optparse
    import sys

    prs = optparse.OptionParser(
        usage="%prog [-s <default>] [-d <path>]")

    prs.add_option('-b', '--backup',
                   dest='backup',
                   action='store_true',
                   help="Run the backup")

    prs.add_option('-l', '--list-sets',
                   dest='list_backup_sets',
                   action='store_true',
                   help='List the available backup sets')

    prs.add_option('-s', '--backup-set',
                   dest='backup_sets',
                   action='append',
                   help='Backup configuration set')
    prs.add_option('-d', '--directory',
                   dest='backup_directory',
                   action='store',
                   default='backups/ab/',
                   help='Directory in which to store backup.ab file')

    prs.add_option('-v', '--verbose',
                    dest='verbose',
                    action='store_true',)
    prs.add_option('-q', '--quiet',
                    dest='quiet',
                    action='store_true',)
    prs.add_option('-t', '--test',
                    dest='run_tests',
                    action='store_true',)

    args = args and list(args) or sys.argv[1:]
    (opts, args) = prs.parse_args()

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)


    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        sys.exit(unittest.main())

    if opts.list_backup_sets:
        import pprint
        for key, value in get_backup_sets(path=opts.backup_directory).items():
            print(key)
            print("=" * len(key))
            print(' '.join(adb_backup_cmd(**value)[0]))
            print(pprint.pformat(value))
        sys.exit(0)

    return android_backup(
        path=opts.backup_directory,
        backup_sets=opts.backup_sets)

if __name__ == "__main__":
    import sys
    sys.exit(main())
