#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``module`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=wrong-import-order
"""

try:
    from .base import TestBase
    from .testlibs import msgs
    # from .testlibs.utilities import utilities
except ImportError:
    from base import TestBase
    from testlibs import msgs
    # from testlibs.utilities import utilities


class TestModule(TestBase):
    """Testing class used to test the ``module`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='')

    # def setUp(self):
    #     """Run this logic *before* each test case."""
    #     self.disable_terminal_output()

    # def tearDown(self):
    #     """Run this logic *after* each test case."""
    #     self.enable_terminal_output()

    def test01__methodname(self):
        """Test the ``method`` method.

        :Test:
            - How this test operates ...

        """
        # inp = []
        # exp = []
        # for i, e in zip(inp, exp):
            # test = <method_call>(i)
            # utilities.assert_true(expected=e, test=test, msg=self._MSG1)
