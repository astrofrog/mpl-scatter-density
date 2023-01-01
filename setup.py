#!/usr/bin/env python

import sys
from packaging.version import Version

try:
    import setuptools
    assert Version(setuptools.__version__) >= Version('30.3')
except (ImportError, AssertionError):
    sys.stderr.write("ERROR: setuptools 30.3 or later is required\n")
    sys.exit(1)

from setuptools import setup

setup(use_scm_version=True)
