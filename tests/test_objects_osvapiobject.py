#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``objects/osvapiobject`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error
# pylint: disable=no-name-in-module
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
from ppklib.objects.osvapiobject import OSVAPIObject


class TestOSVAPIObject(TestBase):
    """Testing class used to test the ``objects/osvapiobject`` module.

    Note:
        The ``.rawjson`` attribute value is not tested in this module
        as OSV can update the raw source at anytime causing these tests
        to fail by external means.

    """

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='objects/osvapiobject')

    def test01a__object__name(self):
        """Test the object attributes with the name argument.

        :Test:
            - Verify the object attributes are as expected.

        """
        oapi = OSVAPIObject(name='utils4')
        self.assertEqual(oapi.name, 'utils4')
        self.assertEqual(oapi.rawjson, {})
        self.assertEqual(oapi.status_code, 0)
        self.assertEqual(oapi.version, None)
        self.assertEqual(oapi.vulns, [])
        self.assertEqual(oapi.wheel, None)

    def test01b__object__name_verison(self):
        """Test the object attributes with the name and version arguments.

        :Test:
            - Verify the object attributes are as expected.

        """
        oapi = OSVAPIObject(name='utils4', version='1.7.0')
        self.assertEqual(oapi.name, 'utils4')
        self.assertEqual(oapi.rawjson, {})
        self.assertEqual(oapi.status_code, 0)
        self.assertEqual(oapi.version, '1.7.0')
        self.assertEqual(oapi.vulns, [])
        self.assertEqual(oapi.wheel, None)

    def test01c__object__wheel(self):
        """Test the object attributes with the wheel argument.

        :Test:
            - Verify the object attributes are as expected.

        """
        oapi = OSVAPIObject(wheel='utils4-1.7.0-cp312-cp312-win_amd64.whl')
        self.assertEqual(oapi.name, 'utils4')
        self.assertEqual(oapi.rawjson, {})
        self.assertEqual(oapi.status_code, 0)
        self.assertEqual(oapi.version, '1.7.0')
        self.assertEqual(oapi.vulns, [])
        self.assertEqual(oapi.wheel, 'utils4-1.7.0-cp312-cp312-win_amd64.whl')

    def test01d__object__version(self):
        """Test the object attributes with the version argument.

        :Test:
            - Verify a ValueError is raised for the invalid argument
              combination.

        """
        with self.assertRaises(ValueError):
            OSVAPIObject(version='1.7.0')

    def test01e__object__targz(self):
        """Test the object attributes with a .tar.gz 'wheel' argument.

        :Test:
            - Verify the name and version are derived correctly for a
              ``.tar.gz`` source file.

        """
        oapi = OSVAPIObject(wheel='utils4-1.7.0.tar.gz')
        self.assertEqual(oapi.name, 'utils4')
        self.assertEqual(oapi.version, '1.7.0')

    def test01f__object__wheel_invalid(self):
        """Test the object attributes with an invalid file extension
        'wheel' argument.

        :Test:
            - Verify a ValueError is raised for a non source or wheel
              file extension.

        """
        with self.assertRaises(ValueError):
            OSVAPIObject(wheel='anything.ext')

    def test02a__get__name(self):
        """Test the ``get`` method with the name argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with only the ``name`` parameter.

        """
        oapi = OSVAPIObject(name='numpy')
        tst = oapi.get()
        self.assertEqual(tst, True)
        self.assertEqual(oapi.rawjson['vulns'][0]['affected'][0]['package']['name'], 'numpy')
        self.assertEqual(oapi.status_code, 200)

    def test02b__get__name_version(self):
        """Test the ``get`` method with the name and version arguments.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``name`` and ``version`` parameters.

        """
        oapi = OSVAPIObject(name='numpy', version='1.20.0')
        tst = oapi.get()
        self.assertEqual(tst, True)
        self.assertEqual(oapi.rawjson['vulns'][0]['affected'][0]['package']['name'], 'numpy')
        self.assertEqual(oapi.version, '1.20.0')
        self.assertEqual(oapi.vulns, [])
        self.assertEqual(oapi.status_code, 200)

    def test02c__get__wheel(self):
        """Test the ``get`` method with the wheel argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``wheel`` parameter.
            - Verify the number of reported vunerabilities is as
              expected.

        """
        w = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oapi = OSVAPIObject(wheel=w)
        tst = oapi.get()
        self.assertEqual(tst, True)
        self.assertEqual(oapi.wheel, w)
        self.assertEqual(oapi.status_code, 200)
        self.assertEqual(len(oapi.rawjson['vulns']), 2)

    def test02d__get__invalid(self):
        """Test the ``get`` method for an invalid library name and verison.

        :Test:
            - Verify the class attribute values are as expected.

        """
        oapi = OSVAPIObject(name='libjamesbond_', version='0.0.7')
        oapi.get_and_filter()
        self.assertEqual(oapi.rawjson, {})
        self.assertEqual(oapi.vulns, [])
        self.assertEqual(oapi.status_code, 200)

    def test02e__get__invalid_error(self):
        """Test the ``get`` method for an invalid library name and verison.

        Note:
            In order to trigger this error, the config is hacked with an
            invalid URL.

        :Test:
            - Verify the appropriate error message is displayed.

        """
        # pylint: disable=import-outside-toplevel
        # Import the module so the config can be hacked.
        from ppklib.objects import osvapiobject
        buf = io.StringIO()
        # Store the original config.
        _cfg = osvapiobject.syscfg['api']['osv']['url']
        # Hack the URL in the module's imported config.
        osvapiobject.syscfg['api']['osv']['url'] = 'https://api.osv.dev/vX/query'  # Invalid
        oapi = osvapiobject.OSVAPIObject(name='libjamesbond_', version='0.0.7')
        with contextlib.redirect_stdout(buf):
            oapi.get_and_filter()
            tst = buf.getvalue()
        self.assertIn('[ERROR]: Request error 404 (Not Found) for "libjamesbond_" v0.0.7.', tst)
        # Restore config.
        osvapiobject.syscfg['api']['osv']['url'] = _cfg

    def test03b__get_and_filter__name_version(self):
        """Test the ``get_and_filter`` method with the name and version
        arguments.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``name`` and ``version`` parameters.

        """
        me = inspect.stack()[0].function
        oapi = OSVAPIObject(name='numpy', version='1.20.0')
        oapi.get_and_filter()
        exp = self.read_data(method=me)
        self.assertEqual(oapi.vulns, exp)

    def test03c__get_and_filter__wheel(self):
        """Test the ``get_and_filter`` method with the wheel argument.

        :Test:
            - Verify the attributes are as expected for a method call
              with the ``wheel`` parameter.

        """
        me = inspect.stack()[0].function
        w = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oapi = OSVAPIObject(wheel=w)
        oapi.get_and_filter()
        exp = self.read_data(method=me)
        self.assertEqual(oapi.vulns, exp)

    def test03d__get_and_filter__counts(self):
        """Test the ``get_and_filter`` method with the wheel argument.

        :Test:
            - Verify the ``counts`` attribute is as expected for a
              method call with the ``wheel`` parameter.

        """
        me = inspect.stack()[0].function
        # This release has 10 reported vulnerabilities.
        w = 'numpy-1.13.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oapi = OSVAPIObject(wheel=w)
        oapi.get_and_filter()
        expobj = self.read_data(method=me)
        attrs = (a for a in dir(oapi.counts) if not a.startswith('_'))
        for attr in attrs:
            with self.subTest(msg=f'{attr=}'):
                exp, tst = getattr(expobj, attr), getattr(oapi.counts, attr)
                self.assertEqual(exp, tst)

    def test05a__repr__none(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        oapi = OSVAPIObject(name='utils4')
        tst = oapi.__repr__()
        exp = '<OSVAPIObject: utils4 Data: None>'
        self.assertEqual(exp, tst)

    def test05b__repr__raw(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        oapi = OSVAPIObject(name='numpy')
        oapi.get()
        tst = oapi.__repr__()
        exp = '<OSVAPIObject: numpy Data: Raw>'
        self.assertEqual(exp, tst)

    def test05c__repr__vulnerabilities(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        oapi = OSVAPIObject(name='numpy', version='1.20.0')
        oapi.get_and_filter()
        tst = oapi.__repr__()
        exp = '<OSVAPIObject: numpy v1.20.0 Data: Vulnerabilities>'
        self.assertEqual(exp, tst)

    def test05e__repr__release(self):
        """Test the ``__repr__`` to verify the object display.

        :Test:
            - Verify the ``__repr__`` method derives the expected output
              based on the arguments.

        """
        w = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
        oapi = OSVAPIObject(wheel=w)
        oapi.get_and_filter()
        tst = oapi.__repr__()
        exp = '<OSVAPIObject: numpy v1.20.0 Data: Vulnerabilities>'
        self.assertEqual(exp, tst)
