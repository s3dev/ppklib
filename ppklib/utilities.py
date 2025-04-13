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
# pylint: disable=wrong-import-order

import getpass
import os
import re
import requests
import sys
import sysconfig


class Utilities:
    """General utility functions wrapper class."""

    @staticmethod
    def get_desktop() -> str:
        """Get the path to the user's Desktop. Works for Linux or Windows.

        Returns:
            str: The full path to the current user's Desktop, per the
            OS-specific environment variable.

        """
        if 'win' in sys.platform:
            return os.path.join(os.environ.get('USERPROFILE'), 'Desktop')
        return os.path.join(os.environ.get('HOME'), 'Desktop')

    @staticmethod
    def get_platform() -> str:
        """Return the current platform."""
        os_, arch_ = sysconfig.get_platform().split('-')
        os_ = 'manylinux2014' if os_ == 'linux' else os_
        return f'{os_}_{arch_}'

    @staticmethod
    def get_python_version() -> str:
        """Return the no-dot major minor python version.

        For example:
            - Python 3.11.x is returned as: 311
            - Python 3.12.x is returned as: 312
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

    @staticmethod
    def normalise_name(name: str) -> str:
        """Normalise the package name per PyPA.

        Args:
            name (str): Package name.

        Reference:
            - https://packaging.python.org/en/latest/specifications/
              name-normalization/#name-normalization

        Deviation:
            This method deviates slightly from the specification in that
            the listed characters are replaced with an *underscore*
            (rather than a hyphen) in efforts to match the name of the
            downloaded wheel file.

        Returns:
            str: Normalised package name.

        """
        return re.sub(r"[-_.]+", "_", name).lower()

    @staticmethod
    def query_pypi(pkg: str) -> dict:
        """Query the PyPI API and get the JSON for the specific package.

        The PyPI API is queried to obtain the data for the requested
        package. If successful, the returned data (in JSON format) is
        stored into the class' ``_json`` variable.

        A timeout of N seconds is setup on the GET request, in the event
        the remote server fails to respond.

        Args:
            pkg (str): Name of the package to be queried.

        Returns:
            dict: The results of the query in JSON format.

        """
        data = None
        url = f'https://pypi.org/pypi/{pkg}/json'
        with requests.get(url, timeout=5) as r:
            if r.status_code == 200:
                data = r.json()
            else:
                msg = (f'\nThe request for ({pkg}) failed with status code: {r.status_code}\n'
                       'Perhaps the package has a different name?')
                raise RuntimeWarning(msg)
        return data


utilities = Utilities()
