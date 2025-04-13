#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module contains generalised utility-based functions,
            used throughout the project.

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""
# pylint: disable=line-too-long  # URL
# pylint: disable=wrong-import-order

import getpass
import os
import re
import sys
import sysconfig


class Utilities:
    """General utility functions wrapper class."""

    @staticmethod
    def get_desktop() -> str:
        """Get the path to the user's Desktop.

        Returns:
            str: The full path to the current user's Desktop.

        """
        return os.path.expanduser('~/Desktop')

    @staticmethod
    def get_platform() -> str:
        """Return the current platform."""
        os_, arch_ = sysconfig.get_platform().split('-')
        os_ = 'manylinux2014' if os_ == 'linux' else os_
        return f'{os_}_{arch_}'

    @staticmethod
    def get_python_version() -> str:
        """Return the no-dot major minor python version.

        This will be the version of the Python executable used to import
        this library, e.g. the ``python.exe`` for *this* environment.

        For example:
            - Python 3.11.x is returned as: ``'311'``
            - Python 3.12.x is returned as: ``'312'``
            - etc.

        """
        ma, mi, *_ = sys.version_info
        return f'{ma}{mi}'

    @staticmethod
    def get_username() -> str:
        """Get the username.

        Returns:
            str: The username for the current user.

        """
        # if 'win' in sys.platform:
        #     return os.environ.get('USERNAME')
        # return os.environ.get('USER')
        return getpass.getuser()

    # # TODO: Move this into utils4.futils.
    # @staticmethod
    # def is_gzip(path: str) -> bool:
    #     """Test if a file is a GZIP compressed file.

    #     Args:
    #         path (str): Full path to the file to be tested.

    #     Returns:
    #         bool: True if the file's binary siganture matches a GZIP
    #         file, otherwise False.

    #     """
    #     with open(path, 'rb') as f:
    #         sig = f.read(2)
    #     return sig == b'\x1f\x8b'

    @staticmethod
    def normalise_name(name: str) -> str | None:
        """Normalise the package name per PyPA.

        Args:
            name (str): Package name.

        Reference:
            - https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization

        Deviation:
            This method deviates slightly from the specification in that
            the listed characters are replaced with an *underscore*
            (rather than a hyphen) in efforts to match the name of the
            downloaded wheel file.

        Returns:
            str: Normalised package name.

        """
        if name:
            return re.sub(r"[-_.]+", "_", name).lower()
        return None


utilities = Utilities()
