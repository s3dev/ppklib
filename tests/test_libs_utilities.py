#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``utilities`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error

try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
import os
import sys
import sysconfig
# locals
from ppklib.libs.utilities import utilities


class TestUtilities(TestBase):
    """Testing class used to test the ``utilities`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='utilities')

    def test01a__get_desktop(self):
        """Test the ``get_desktop`` method.

        :Test:
            - Verify the function returns the expected result.

        """
        tst = utilities.get_desktop()
        exp = self._DIR_DSK
        self.assertEqual(exp, tst)

    def test02a__get_platform(self):
        """Test the ``get_platform`` method.

        :Test:
            - Verify the function returns the expected result.

        """
        exp = None
        tst = utilities.get_platform()
        if sys.platform == 'linux':
            arch = sysconfig.get_platform().split('-')[1]
            exp = f'manylinux2014_{arch}'
        elif sys.platform == 'win32':
            exp = sysconfig.get_platform().replace('-', '_')
        self.assertEqual(exp, tst)

    def test03a__get_python_version(self):
        """Test the ``get_python_version`` method.

        :Test:
            - Verify the function returns the expected result.

        """
        tst = utilities.get_python_version()
        maj_, min_, *_ = sys.version_info
        exp = f'{maj_}{min_}'
        self.assertEqual(exp, tst)

    def test04a__get_username(self):
        """Test the ``get_username`` method.

        :Test:
            - Verify the function returns the expected result.

        """
        exp = None
        tst = utilities.get_username()
        if sys.platform == 'linux':
            exp = os.environ.get('USER')
        elif sys.platform == 'win32':
            exp = os.environ.get('USERNAME')
        self.assertEqual(exp, tst)

    def test05a__normalise_name(self):
        """Test the ``normalise_name`` method.

        :Test:
            - Verify the function returns the expected result.

        """
        pairs = (
                 ('MIXEDcase', 'mixedcase'),
                 ('MIX-with-hyphen', 'mix_with_hyphen'),
                 ('MIX-with-hyphen_and_under', 'mix_with_hyphen_and_under'),
                 ('MIX.with.dots', 'mix_with_dots'),
                 ('SomeTHing.that--Is--just-.__.-SILL.y', 'something_that_is_just_sill_y')
                )
        for name, exp in pairs:
            tst = utilities.normalise_name(name=name)
            with self.subTest(msg=f'{tst}, {exp}'):
                self.assertEqual(exp, tst)
