#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``vtests`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error

import contextlib
import inspect
import io
import os
from glob import glob
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppklib.vtests import VTests


class TestVTests(TestBase):
    """Testing class used to test the ``vtests`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='vtests')

    def test01a__md5__pass(self):
        """Test the ``md5`` method.

        :Test:
            - For several different wheels, verify the calculated MD5 sum
              matches that of PyPI.

        """
        wheels = glob(os.path.join(self._DIR_RESC, '*.whl'))
        for w in wheels:
            base = os.path.basename(w)
            pkg, vers, *_ = base.split('-')
            with self.subTest(msg=f'{pkg}-{vers}'):
                tst = VTests.md5(fpath=w, name=pkg, version=vers)
                self.assertTrue(tst[0])

    def test02a__snyk__pass(self):
        """Test the ``snyk`` method for a passing library.

        :Test:
            - Verify the Snyk check passes for a known 'good' library.

        """
        buf = io.StringIO()
        exp1 = (True, 0, 0, 0, 0)
        exp2 = 'preqs v0.1.0 has no reported direct vulnerabilities, per Snyk\n'
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.snyk('preqs', '0.1.0', verbose=False)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(exp2, tst2)

    def test02b__snyk__minor_fail(self):
        """Test the ``snyk`` method for a minor failing library.

        :Test:
            - Verify the Snyk check passes for a known library which
              will pass, but has reported vulnerabilities.

        """
        buf = io.StringIO()
        exp1 = (True, 0, 0, 0, 4)
        exp2 = ''
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.snyk('numpy', '1.16.3', verbose=False)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(exp2, tst2)

    def test02c__snyk__minor_fail_verbose(self):
        """Test the ``snyk`` method for a minor failing library, verbose.

        :Test:
            - Verify the Snyk check passes for a known library which
              will pass, but has reported vulnerabilities - in verbose
              mode.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        exp1 = (True, 0, 0, 0, 4)
        with open(os.path.join(self._DIR_RESC, f'{me}.txt'), encoding='utf-8') as f:
            exp2 = f.read()
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.snyk('numpy', '1.16.3', verbose=True)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(sorted(exp2), sorted(tst2))  # The vulns are displayed in diff orders.

    def test02d__snyk__major_fail_verbose(self):
        """Test the ``snyk`` method for a major failing library, verbose.

        :Test:
            - Verify the Snyk check passes for a known library which
              will fail with reported vulnerabilities - in verbose mode.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        exp1 = (False, 1, 1, 0, 4)
        with open(os.path.join(self._DIR_RESC, f'{me}.txt'), encoding='utf-8') as f:
            exp2 = f.read()
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.snyk('numpy', '1.13.1', verbose=True)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(sorted(exp2), sorted(tst2))  # The vulns are displayed in diff orders.

    def test03a__osv__pass(self):
        """Test the ``osv`` method for a passing library.

        :Test:
            - Verify the OSV check passes for a known 'good' library.

        """
        buf = io.StringIO()
        exp1 = (True, 0, 0, 0, 0)
        exp2 = 'preqs v0.1.0 has no reported direct vulnerabilities, per OSV\n'
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.osv(name='preqs', version='0.1.0', verbose=False)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(exp2, tst2)

    def test03b__osv__minor_fail(self):
        """Test the ``osv`` method for a minor failing library.

        :Test:
            - Verify the OSV check passes for a known library which
              will pass, but has reported vulnerabilities.

        """
        buf = io.StringIO()
        exp1 = (False, 0, 1, 5, 0)
        exp2 = ''
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.osv(name='numpy', version='1.16.3', verbose=False)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(exp2, tst2)

    def test03c__osv__minor_fail_verbose(self):
        """Test the ``osv`` method for a minor failing library, verbose.

        :Test:
            - Verify the OSV check passes for a known library which
              will pass, but has reported vulnerabilities - in verbose
              mode.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        exp1 = (False, 0, 1, 5, 0)
        with open(os.path.join(self._DIR_RESC, f'{me}.txt'), encoding='utf-8') as f:
            exp2 = f.read()
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.osv(name='numpy', version='1.16.3', verbose=True)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(sorted(exp2), sorted(tst2))  # The vulns are displayed in diff orders.

    def test03d__osv__major_fail_verbose(self):
        """Test the ``osv`` method for a major failing library, verbose.

        :Test:
            - Verify the OSV check passes for a known library which
              will fail with reported vulnerabilities - in verbose mode.

        """
        me = inspect.stack()[0].function
        buf = io.StringIO()
        exp1 = (False, 1, 6, 3, 0)
        with open(os.path.join(self._DIR_RESC, f'{me}.txt'), encoding='utf-8') as f:
            exp2 = f.read()
        with contextlib.redirect_stdout(buf):
            tst1 = VTests.osv(name='numpy', version='1.13.1', verbose=True)
            tst2 = buf.getvalue()
        self.assertEqual(exp1, tst1)
        self.assertEqual(sorted(exp2), sorted(tst2))  # The vulns are displayed in diff orders.
