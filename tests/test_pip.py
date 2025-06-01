#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   Testing module for the ``pip`` module.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=import-error

import contextlib
import io
import os
import shutil
try:
    from .base import TestBase
    from .testlibs import msgs
except ImportError:
    from base import TestBase
    from testlibs import msgs
# locals
from ppklib.pip import Download


class TestDownload(TestBase):
    """Testing class used to test the ``pip.Download`` class."""

    _MSG1 = msgs.templates.not_as_expected.general

    @classmethod
    def setUpClass(cls):
        """Run this logic at the start of all test cases."""
        msgs.startoftest.startoftest(module_name='pip.Download')

    # def setUp(self):
    #     """Run this logic *before* each test case."""
    #     self.disable_terminal_output()

    # def tearDown(self):
    #     """Run this logic *after* each test case."""
    #     self.enable_terminal_output()

    def test01a__get(self):
        """Test the ``get`` method.

        :Test:
            - Perform a download with minimal arguments.
            - Verify the wheel was downloaded.
            - Call cleanup.
            - Verify the wheel no longer exists.

        """
        d = Download('preqs')
        d.get()
        self.assertTrue(os.path.exists(d.pkgpath))
        d.cleanup()
        self.assertFalse(os.path.exists(d.pkgpath))

    def test01b__get__tmpdir(self):
        """Test the ``get`` method with a specific temp directory.

        :Test:
            - Perform a download with minimal arguments.
            - Verify the wheel was downloaded.
            - Call cleanup.
            - Verify the wheel no longer exists.

        """
        tmpdir = os.path.join(self._DIR_DSK, 'tempc0ff33')
        d = Download('preqs', tmpdir=tmpdir)
        d.get()
        self.assertTrue(os.path.exists(d.pkgpath))
        d.cleanup()
        self.assertFalse(os.path.exists(d.pkgpath))

    def test01c__get__utils4_vers_win(self):
        """Test the ``get`` method with a specific version of utils4.

        :Test:
            - Perform a download with arguments.
            - Verify the wheel was downloaded.
            - Call cleanup.
            - Verify the wheel no longer exists.

        """
        d = Download('utils4', version='1.5.0', args={'platform': 'win_amd64',
                                                      'python_version': '310'})
        d.get()
        self.assertTrue(os.path.exists(d.pkgpath))
        d.cleanup()
        self.assertFalse(os.path.exists(d.pkgpath))

    def test01d__get__utils4_vers_win_no_deps(self):
        """Test the ``get`` method with a specific version of utils4.

        :Test:
            - Perform a download with arguments, specifically 'no_deps'
            - Verify *only* the target wheel was downloaded.
            - Call cleanup.
            - Verify the wheel no longer exists.

        """
        # pylint: disable=protected-access
        d = Download('utils4', version='1.5.0', args={'platform': 'win_amd64',
                                                      'python_version': '310',
                                                      'no_deps': True})
        d.get()
        nfiles = len(os.listdir(d._tmpdirname))
        self.assertTrue(os.path.exists(d.pkgpath))
        self.assertEqual(1, nfiles)
        d.cleanup()
        self.assertFalse(os.path.exists(d.pkgpath))

    def test01e__get__preqs_invalid(self):
        """Test the ``get`` method for an invalid library.

        :Test:
            - Perform a download with an invalid version.
            - Verify the error message is as expected and the package
              path is set to None.

        """
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            d = Download('preqs', version='0.0.0')
            d.get()
            d.cleanup()  # Address the potential ResourceWarning
            tst1 = d.pkgpath
            tst2 = buf.getvalue()
        self.assertIsNone(tst1)
        self.assertIn('ERROR: Could not find a version that satisfies the requirement', tst2)
        self.assertIn('ERROR: No matching distribution found for preqs==0.0.0', tst2)

    def test01f__get__reqfile_invalid(self):
        """Test the ``get`` method for an invalid requirements file.

        :Test:
            - Perform a download with a requirements file and platform
              which forces the requirements file to be updated
              internally.

        """
        path = os.path.join(self._DIR_RESC, 'requirements.txt')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            d = Download(None,
                         reqfile=path,
                         args={'platform': 'manylinux2014_x86_64'})
            d.get()
            tst1 = os.path.exists(d.pkgpath)
            d.cleanup()
            tst2 = os.path.exists(d.pkgpath)
            tst3 = buf.getvalue()
        # Restore the original requirements file.
        shutil.copy(f'{path}.bak', path)
        self.assertTrue(tst1)
        self.assertFalse(tst2)
        self.assertIn('ERROR: Could not find a version that satisfies the requirement', tst3)
        self.assertIn('Modifying the requirements file and trying again', tst3)
