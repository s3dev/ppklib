#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``pypi`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module  # ppklib.osv (Yes there is)

import contextlib
import inspect
import math
import os
try:
    from .base import TestBase, _DEVMODE
    from .testlibs import msgs
except ImportError:
    from base import TestBase, _DEVMODE
    from testlibs import msgs
# locals
from ppklib.pypi import PyPIQuery


class TestPyPI(TestBase):
    """Testing class used to test the ``pypi`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='pypi')

    def test01a__metadata(self):
        """Test the ``metadata`` method.

        :Test:
            - Verify the retrieved and filtered metadata is as expected.

        """
        me = inspect.stack()[0].function
        meta = PyPIQuery.metadata(name='utils4', version='1.5.0')
        exp = self.read_data(method=me)
        # The latest version will change -->
        meta.data.pop('latest_version')
        exp.pop('latest_version')
        self.assertEqual(exp, meta.data)

    def test01b__metadata__invalid(self):
        """Test the ``metadata`` method with invalid arguments.

        :Test:
            - Verify the return value is None.

        """
        with contextlib.redirect_stdout(None):
            meta = PyPIQuery.metadata()
        self.assertEqual(None, meta)

    def test02a__metadata__repo(self):
        """Test the ``metadata`` method in a loop against a repo.

        This test is designed to test *many* wheel and source file
        variations against the metadata compilation logic to help expose
        any corner cases in naming convention.

        :Test:
            - Verify the length of the metadata list is as expected.
            - Verify all of the metadata repr's show 'Metadata (release).

        """
        step = 1  # Must be 1 on final tests. Can change to 50 for a fast test.
        expcount = 273
        if _DEVMODE:
            step = 50
            expcount = math.ceil(expcount/step)
            print(f'\n\n[WARNING]: Step is set to {step}. This must be one (1) before releasing.')
        m = []
        with open(os.path.join(self._DIR_RESC, 'repo.txt'), encoding='utf-8') as f:
            files = [line.strip() for line in f][::step]
        total = len(files)
        print(f'\nTesting {total} filenames. This will take a couple minutes ...')
        for idx, f in enumerate(files, 1):
            if not idx % 20:
                print(f'- {idx} of {total}')
            m.append(PyPIQuery.metadata(wheel=f))
        tst1 = len(m)
        tst2 = all(map(lambda x: 'Metadata (release)' in repr(x), m))
        self.assertEqual(expcount, tst1)
        self.assertTrue(tst2)
