#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_docutils

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_docutils.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-docutils',
    version=version,
    description="""Docutils (reStructuredText) support for Django""",
    long_description=readme + '\n\n' + history,
    author='Tony Narlock',
    author_email='tony@git-pull.com',
    url='https://github.com/tony/django-docutils',
    packages=[
        'django_docutils',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-docutils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
