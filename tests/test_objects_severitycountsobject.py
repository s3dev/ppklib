#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``objects/severitycountsobject``
            module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module         # ppklib.OSVQuery (Defined in ppklib.__init__)
# pylint: disable=unnecessary-dunder-call   # Calling the method explicitly.

import inspect
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppklib import OSVQuery
from ppklib.objects.severitycountsobject import SeverityCountsObject


class TestSeverityCountsObject(TestBase):
    """Testing class for the ``objects/severitycountsobject`` module."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='objects/severitycountsobject')

    def test01a__counts__empty(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with no reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [{}]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test01b__counts__low(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [{'severity': 'LoW'}]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test01c__counts__medium(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [{'severity': 'MEDium'}, {'severity': 'MODERatE'}]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test01d__counts__high(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [{'severity': 'HIGh'}]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test01e__counts__critical(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [{'severity': 'CRitiCal'}]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test02a__counts__multiple(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with multiple reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        vulns = [
                 {'severity': 'low', 'key': 'spam'},
                 {'severity': 'moderate', 'key': 'and'},
                 {'severity': 'high', 'key': 'eggs'},
                 {'severity': 'critical', 'key': 'spamspamspam'},
                ]
        tst = SeverityCountsObject(vulns=vulns)
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test03a__counts__numpy(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with multiple reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        w = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oquery = OSVQuery.vulnerabilities(wheel=w)
        tst = oquery.counts
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test03b__counts__numpy(self):
        """Test the various count properties of the class.

        :Test:
            - Verify the various count properties are as expected for a
              module with multiple reported vulnerabilities.

        """
        me = inspect.stack()[0].function
        w = 'numpy-1.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oquery = OSVQuery.vulnerabilities(wheel=w)
        tst = oquery.counts
        exp = self.read_data(method=me)
        self._test_all(expobj=exp, tstobj=tst)

    def test04b__repr__numpy(self):
        """Test the __repr__ method to ensure correct display.

        :Test:
            - Verify the ``__repr__`` method displays the expected
              counts.

        """
        w = 'numpy-1.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oquery = OSVQuery.vulnerabilities(wheel=w)
        tst = oquery.counts.__repr__()
        exp = '<SeverityCountsObject> C: 1, H: 6, M: 3, L: 0 (Total: 10)'
        self.assertEqual(exp, tst)

    def test05a__iter__numpy(self):
        """Test the __iter__ method to ensure correct object.

        :Test:
            - Verify the ``__iter__`` method creates the expected
              iterable object.

        """
        w = 'numpy-1.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oquery = OSVQuery.vulnerabilities(wheel=w)
        tst1 = tuple(oquery.counts)
        tst2 = list(oquery.counts)
        exp1 = (1, 6, 3, 0)
        exp2 = [1, 6, 3, 0]
        with self.subTest('Tuple'):
            self.assertEqual(exp1, tst1)
        with self.subTest('List'):
            self.assertEqual(exp2, tst2)


# %% Test helper methods

    def _test_all(self, expobj: SeverityCountsObject, tstobj: SeverityCountsObject) -> None:
        """Test all public attributes for the exp and tst objects."""
        attrs = (a for a in dir(SeverityCountsObject) if not a.startswith('_'))
        for attr in attrs:
            with self.subTest(msg=f'{attr=}'):
                exp, tst = getattr(expobj, attr), getattr(tstobj, attr)
                self.assertEqual(exp, tst)
