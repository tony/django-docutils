#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

about = {}
with open("django_docutils/__about__.py") as fp:
    exec(fp.read(), about)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print(
        "  git tag -a %s -m 'version %s'" % (about['__version__'], about['__version'])
    )
    print("  git push --tags")
    sys.exit()


readme = open('README.rst').read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    long_description=readme,
    author_email=about['__email__'],
    description=about['__description__'],
    packages=['django_docutils',],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords=[
        'django',
        'docutils',
        'documentation utilities',
        'reST',
        'reStructuredText',
        'rst',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
