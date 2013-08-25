#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # lint:ok

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='qtfeet',
    version='0.1.0',
    description='QTFeet, DBus instrospection tool, DFeet clone writed with QT',
    long_description=readme + '\n\n' + history,
    author='hugosenari',
    author_email='hugosenari@gmail.com',
    url='https://github.com/hugosenari/qtfeet',
    packages=[
        'qtfeet',
    ],
    package_dir={'qtfeet': 'qtfeet'},
    include_package_data=True,
    install_requires=[
        'iPOPO'
    ],
    license="BSD",
    zip_safe=False,
    keywords='qtfeet',
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