#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the superclass which is to be inherited
            by the test-specific modules.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Example:
    Example code use.


    Run all tests via the shell script::

        $ ./run.sh


    Run all tests under coverage::

        $ ./coverage.sh


    Run all tests using unittest::

        $ python -m unittest discover


    Run a single test::

        $ python -m unittest test_name.py

"""
# pylint: disable=wrong-import-position

# Set path for relative imports.
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import io
import pickle
import unittest
# locals
try:
    from .testlibs import msgs
except ImportError:
    from testlibs import msgs

# Must be False for production builds.
_DEVMODE = True

if _DEVMODE:
    msgs.msgs.print_devmode()


class TestBase(unittest.TestCase):
    """Private generalised base-testing class.

    This class is designed to be inherited by each test-specific class.

    There is no special functionality provided by this class at this time.

    """

    _DIR_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    _DIR_DSK = os.path.expanduser('~/Desktop')
    _DIR_RESC = os.path.join(_DIR_ROOT, 'tests/resources')
    if 'linux' in sys.platform.lower():
        _DIR_TMP = '/tmp'
    elif 'win' in sys.platform.lower():
        _DIR_TMP = 'c:/temp'
    else:
        _DIR_TMP = None

    @staticmethod
    def disable_terminal_output():
        """Turn off all output to the terminal."""
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

    @staticmethod
    def enable_terminal_output():
        """Turn on output to the terminal."""
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def read_data(self, method: str) -> object:
        """Read the serialised file for the given test method.

        Args:
            method (str): Name of the test method. The serialised files
                are named after their test method.

        Returns:
            object: The object contained in the serialised file.

        """
        path = os.path.join(self._DIR_RESC, f'{method}.p')
        with open(path, 'rb') as f:
            data = pickle.load(f)
        return data
