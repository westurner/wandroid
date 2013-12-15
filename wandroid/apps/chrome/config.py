#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
"""
configure_mobile_chrome_preferences
"""
import json

import wandroid.adbw as adbw

CHROME_PREFS = '/data/data/com.android.chrome/app_chrome/Default/Preferences'
def update_chrome_config():
    return adbw.update_remote_file(CHROME_PREFS,
                              func=configure_mobile_chrome_preferences)

def get_chrome_config():
    return adbw.get_remote_file(CHROME_PREFS)


def configure_mobile_chrome_preferences(path):
    """
    Configure Android Chrome Preferences JSON file

    - HTTPS search URLS
    - Reset location data permissions
    - Disable camera/microphone
    """
    GOOGLE_BASE_URL = 'https:/www.google.com/'
    contents = None
    with open(path, 'r') as f:
        contents = f.read()

    # these seem to be getting overwritten
    #contents = contents.replace('{google:baseURL}', GOOGLE_BASE_URL)
    #contents = contents.replace('{google:baseSuggestURL}', GOOGLE_BASE_URL)
    contents = contents.replace('http:', 'https:')

    prefs = json.loads(contents)

    # reset geolocation configuration for all configured sites
    if 'profile' not in prefs:
        prefs['profile'] = {}
    if 'content_settings' not in prefs['profile']:
        prefs['profile']['content_settings'] = {}
    if 'pattern_pairs' not in prefs['profile']['content_settings']:
        prefs['profile']['content_settings']['pattern_pairs'] = {}

    for key, value in (
        prefs['profile']['content_settings']['pattern_pairs'].items()):
        if 'geolocation' in value:
            value.pop("geolocation")
        if not value:
            prefs['profile']['content_settings']['pattern_pairs'].pop(key)
        else:
            prefs['profile']['content_settings']['pattern_pairs'][key] = \
                value
            print(value)

    # disable mic/camera access through chrome
    if 'default_content_settings' not in prefs['profile']:
        prefs['profile']['default_content_settings'] = {}

    prefs['profile']['default_content_settings'].update(
        {'media-stream-camera': 2,
         'media-stream-mic': 2})

    # set default browser to httos://www.google.com
    if 'browser' not in prefs:
        prefs['browser'] = {}

    prefs['browser'].update({
        "last_known_google_url": GOOGLE_BASE_URL,
        "last_prompted_google_url": GOOGLE_BASE_URL
    })

    with open(path, 'w') as f:
        json.dump(prefs, f, indent=4)

    return 0



import unittest
class Test_configure_mobile_chrome_preferences(unittest.TestCase):
    def test_configure_mobile_chrome_preferences(self):
        # adb pull [...]/Preferences
        path = './Preferences'
        retval = configure_mobile_chrome_preferences(path)
        self.assertEqual(retval, 0)


def main():
    import optparse
    import logging

    prs = optparse.OptionParser(usage="%prog [ -r | -l <./Preferences> ]")

    prs.add_option('-l', '--local',
                    dest='local',
                    action='store_true',
                    help="Update a local file")
    prs.add_option('-g', '--get',
                    dest='get',
                    action='store_true',
                    help='Retrieve remote Preferences file with adb pull')
    prs.add_option('-r', '--remote',
                    dest='remote',
                    action='store_true',
                    help='Update over adb shell')

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

    if opts.local:
        path = args[0]
        configure_mobile_chrome_preferences(path)
        return 0

    if opts.remote:
        update_chrome_config()
        return 0

    if opts.get:
        filename = get_chrome_config()
        print(filename)
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
