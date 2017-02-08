#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 7):
    print("Python 2.7 or higher required, please upgrade.")
    sys.exit(1)


setup(name='relocate-venv',
      version='0.1',
      description='Make a virtualenv relcoatable on big computers',
      url='http://github.com/firedrakeproject/relocate-venv',
      author='Nick Johnson',
      author_email='n.johnson@epcc.ed.ac.uk',
      license='Apache 2.0',
      packages=['relocate_venv'],
      zip_safe=False)
