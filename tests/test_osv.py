#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``osv`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module  # ppklib.osv (Yes there is)

import contextlib
import inspect
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppklib.osv import OSVQuery


class TestOSV(TestBase):
    """Testing class used to test the ``osv`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='osv')

    def test01a__vulnerabilities_utils4(self):
        """Test the ``vulnerabilities`` method for ``utils4``.

        :Test:
            - Verify the retrieved and filtered vulnerabilities are as
              expected.

        """
        oquery = OSVQuery.vulnerabilities(name='utils4', version='1.7.0')
        exp = []
        self.assertEqual(exp, oquery.vulns)

    def test01b__vulnerabilities_numpy(self):
        """Test the ``vulnerabilities`` method for ``numpy``.

        :Test:
            - Verify the retrieved and filtered vulnerabilities are as
              expected.

        """
        me = inspect.stack()[0].function
        oquery = OSVQuery.vulnerabilities(name='numpy', version='1.20.0')
        exp = self.read_data(method=me)
        self.assertEqual(200, oquery.status_code)
        self.assertEqual(exp, oquery.vulns)

    def test01c__vulnerabilities__invalid(self):
        """Test the ``vulnerabilities`` method with invalid arguments.

        :Test:
            - Verify the return value is None.

        """
        with contextlib.redirect_stdout(None):
            oquery = OSVQuery.vulnerabilities()
        self.assertEqual(None, oquery)
