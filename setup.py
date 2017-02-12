#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools.command.test import test as TestCommand

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

about = {}
with open("django_docutils/__about__.py") as fp:
    exec(fp.read(), about)

with open('requirements/base.txt') as f:
    install_reqs = [line for line in f.read().split('\n') if line]

with open('requirements/test.txt') as f:
    tests_reqs = [line for line in f.read().split('\n') if line]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (
        about['__version__'], about['__version']
    ))
    print("  git push --tags")
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


readme = open('README.rst').read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    long_description=readme,
    author_email=about['__email__'],
    description=about['__description__'],
    packages=[
        'django_docutils',
    ],
    include_package_data=True,
    install_requires=install_reqs,
    tests_require=tests_reqs,
    cmdclass={'test': PyTest},
    license="BSD",
    zip_safe=False,
    keywords=['django,' 'docutils', 'documentation utilities', 'reST',
              'reStructuredText', 'rst'],
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
