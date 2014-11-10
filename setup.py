#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='wandroid',
    version='0.1.0',
    description='Utilities, tools, and scripts for working with Android',
    long_description=readme + '\n\n' + history,
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url='https://bitbucket.org/westurner/wandroid',
    packages=[
        'wandroid',
    ],
    namespace_package=[
        'wandroid',
        'wandroid.devices',
    ],
    package_dir={'wandroid': 'wandroid'},
    scripts=[
        'scripts/setup_adt_sdk.sh',
        'scripts/configure_path.sh',
        'scripts/postactivate',
        'scripts/android_backup.py',
        'scripts/android-eclipse.sh',
    ],
    entry_points={
        'console_scripts': [
            'update-chrome-config = wandroid.apps.chrome.config:main',
            'get-chrome-userdata = wandroid.apps.chrome.userdata:main',
            'wdev = wandroid.devices.utils:main',
    ]},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='android wandroid',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
