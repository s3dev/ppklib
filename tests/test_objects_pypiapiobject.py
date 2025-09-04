#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``objects/pypiapiobject`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=too-many-public-methods  # Ya. Test cases, get over it.
# pylint: disable=unnecessary-dunder-call  # Calling the method explicitly.

import contextlib
import inspect
import io
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppklib.objects.pypiapiobject import PyPIAPIObject


class TestPyPIAPIObject(TestBase):
    """Testing class used to test the ``objects/pypiapiobject`` module.

    Note:
        The ``.rawjson`` attribute value is not tested in this module
        as PyPI can update the raw source at anytime causing these tests
        to fail by external means.

    """

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='objects/pypiapiobject')

    def test01a__object__name(self):
        """Test the object attributes with the name argument.

        :Test:
            - Verify the object attributes are as expected.

        """
        papi = PyPIAPIObject(name='utils4')
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.name, 'utils4')
        self.assertEqual(papi.rawjson, {})
        self.assertEqual(papi.status_code, 0)
        self.assertEqual(papi.version, None)
        self.assertEqual(papi.wheel, None)

    def test01b__object__name_verison(self):
        """Test the object attributes with the name and version arguments.

        :Test:
            - Verify the object attributes are as expected.

        """
        papi = PyPIAPIObject(name='utils4', version='1.7.0')
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.name, 'utils4')
        self.assertEqual(papi.rawjson, {})
        self.assertEqual(papi.status_code, 0)
        self.assertEqual(papi.version, '1.7.0')
        self.assertEqual(papi.wheel, None)

    def test01c__object__wheel(self):
        """Test the object attributes with the wheel argument.

        :Test:
            - Verify the object attributes are as expected.

        """
        papi = PyPIAPIObject(wheel='utils4-1.7.0-cp312-cp312-win_amd64.whl')
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.name, 'utils4')
        self.assertEqual(papi.rawjson, {})
        self.assertEqual(papi.status_code, 0)
        self.assertEqual(papi.version, '1.7.0')
        self.assertEqual(papi.wheel, 'utils4-1.7.0-cp312-cp312-win_amd64.whl')

    def test01d__object__version(self):
        """Test the object attributes with the version argument.

        :Test:
            - Verify a ValueError is raised for the invalid argument
              combination.

        """
        with self.assertRaises(ValueError):
            PyPIAPIObject(version='1.7.0')

    def test01e__object__targz(self):
        """Test the object attributes with a .tar.gz 'wheel' argument.

        :Test:
            - Verify the name and version are derived correctly for a
              ``.tar.gz`` source file.

        """
        papi = PyPIAPIObject(wheel='utils4-1.7.0.tar.gz')
        self.assertEqual(papi.name, 'utils4')
        self.assertEqual(papi.version, '1.7.0')

    def test01f__object__invalid(self):
        """Test the object attributes with an invalid file extension
        'wheel' argument.

        :Test:
            - Verify a ValueError is raised for a non source or wheel
              file extension.

        """
        with self.assertRaises(ValueError):
            PyPIAPIObject(wheel='anything.ext')

    def test02a__get__name(self):
        """Test the ``get`` method with the name argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with only the ``name`` parameter.

        """
        papi = PyPIAPIObject(name='utils4')
        tst = papi.get()
        self.assertEqual(tst, True)
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.rawjson['info']['name'], 'utils4')
        self.assertEqual(papi.status_code, 200)

    def test02b__get__name_version(self):
        """Test the ``get`` method with the name and version arguments.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``name`` and ``version`` parameters.

        """
        papi = PyPIAPIObject(name='utils4', version='1.5.0')
        tst = papi.get()
        self.assertEqual(tst, True)
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.rawjson['info']['name'], 'utils4')
        self.assertEqual(papi.rawjson['info']['version'], '1.5.0')
        self.assertEqual(papi.status_code, 200)

    def test02c__get__wheel(self):
        """Test the ``get`` method with the wheel argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``wheel`` parameter.
            - Verify the ``'urls'`` key of the raw JSON is as expected.

        """
        me = inspect.stack()[0].function
        papi = PyPIAPIObject(wheel='utils4-1.5.0-cp312-cp312-win_amd64.whl')
        tst = papi.get()
        exp = self.read_data(method=me)
        self.assertEqual(tst, True)
        self.assertEqual(papi.data, {})
        self.assertEqual(papi.rawjson['info']['name'], 'utils4')
        self.assertEqual(papi.rawjson['info']['version'], '1.5.0')
        self.assertEqual(papi.rawjson['urls'], exp)
        self.assertEqual(papi.status_code, 200)

    def test02d__get__invalid(self):
        """Test the ``get`` method for an invalid library name and verison.

        :Test:
            - Verify the appropriate error message is displayed.

        """
        buf = io.StringIO()
        papi = PyPIAPIObject(name='libjamesbond_', version='0.0.7')
        with contextlib.redirect_stdout(buf):
            papi.get_and_filter()
            tst = buf.getvalue()
        self.assertIn('[ERROR]: Request error 404 (Not Found) for "libjamesbond_" v0.0.7.', tst)

    def test03a__get_and_filter__name(self):
        """Test the ``get_and_filter`` method with the name argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``name`` parameter.

        """
        me = inspect.stack()[0].function
        papi = PyPIAPIObject(name='utils4')
        papi.get_and_filter()
        exp = self.read_data(method=me)
        # The latest version will change -->
        papi.data.pop('latest_version')
        exp.pop('latest_version')
        self.assertEqual(papi.data, exp)

    def test03b__get_and_filter__wheel(self):
        """Test the ``get_and_filter`` method with the wheel argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``wheel`` parameter.

        """
        me = inspect.stack()[0].function
        papi = PyPIAPIObject(wheel='utils4-1.5.0-cp312-cp312-win_amd64.whl')
        papi.get_and_filter()
        exp = self.read_data(method=me)
        # The latest version will change -->
        papi.data.pop('latest_version')
        exp.pop('latest_version')
        self.assertEqual(papi.data, exp)

    def test03c__get_and_filter__name_version(self):
        """Test the ``get_and_filter`` method with the name and version
        arguments.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``name`` and ``version`` parameters.

        """
        me = inspect.stack()[0].function
        papi = PyPIAPIObject(name='utils4', version='1.5.0')
        papi.get_and_filter()
        exp = self.read_data(method=me)
        # The latest version will change -->
        papi.data.pop('latest_version')
        exp.pop('latest_version')
        self.assertEqual(papi.data, exp)

    def test03d__get_and_filter__vulns(self):
        """Test the ``get_and_filter`` method with the wheel argument.

        :Test:
            - Verify the ``vulns`` attribute is as expected for a
              method call with the ``wheel`` parameter.

        """
        me = inspect.stack()[0].function
        wheel = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        papi = PyPIAPIObject(wheel=wheel)
        papi.get_and_filter()
        exp = self.read_data(method=me)
        self.assertEqual(papi.vulns, exp)

    def test04a__get_and_filter__long_license(self):
        """Test the ``get_and_filter`` method for a long license value.

        :Test:
            - Verify the attributes are as expected for a method call.
            - The 'latest_version' key is removed from the test and
              expected datasets as this will fail test as time goes on.

        """
        me = inspect.stack()[0].function
        papi = PyPIAPIObject(name='numpy', version='2.2.4')
        papi.get_and_filter()
        exp = self.read_data(method=me)
        _ = papi.data.pop('latest_version')
        _ = exp.pop('latest_version')
        self.assertEqual(papi.data, exp)

    def test05a__repr__none(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        papi = PyPIAPIObject(name='utils4')
        tst = papi.__repr__()
        exp = '<PyPIAPIObject: utils4 Data: None>'
        self.assertEqual(exp, tst)

    def test05b__repr__raw(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        papi = PyPIAPIObject(name='utils4')
        papi.get()
        tst = papi.__repr__()
        exp = '<PyPIAPIObject: utils4 Data: Raw>'
        self.assertEqual(exp, tst)

    def test05c__repr__metadata(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        papi = PyPIAPIObject(name='utils4')
        papi.get_and_filter()
        tst = papi.__repr__()
        exp = '<PyPIAPIObject: utils4 Data: Metadata>'
        self.assertEqual(exp, tst)

    def test05d__repr__metadata_version(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        papi = PyPIAPIObject(name='utils4', version='1.5.0')
        papi.get_and_filter()
        tst = papi.__repr__()
        exp = '<PyPIAPIObject: utils4 v1.5.0 Data: Metadata>'
        self.assertEqual(exp, tst)

    def test05e__repr__release(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        papi = PyPIAPIObject(wheel='utils4-1.7.0-cp312-cp312-win_amd64.whl')
        papi.get_and_filter()
        tst = papi.__repr__()
        exp = '<PyPIAPIObject: utils4 v1.7.0 Data: Metadata (release)>'
        self.assertEqual(exp, tst)
