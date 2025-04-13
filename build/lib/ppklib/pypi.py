#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides functionality for interacting with PyPI,
            specifically, the Index and JSON APIs.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:References:

            The following links provide the requirements (specification)
            on which this module's logic and API interactions are based:

                - `PyPI Index API <indexapi_>`_
                - `PyPI JSON API <jsonapi_>`_

:Comments:  n/a

            .. _indexapi: https://docs.pypi.org/api/index-api/
            .. _jsonapi: https://docs.pypi.org/api/json/

"""

import traceback
from utils4.user_interface import ui
# locals
try:
    from .objects.pypiapiobject import PyPIAPIObject
except ImportError:
    from objects.pypiapiobject import PyPIAPIObject


class PyPIQuery:
    """Class for handling PyPI project queries.

    :Examples:

        Query a project's latest metadata from PyPI::

            >>> from ppklib import PyPIQuery

            >>> pquery = PyPIQuery.metadata('utils4')

            >>> # Inspect the retrieved data.
            >>> pquery.data
            {'author': None,
             'author_email': 'The Developers <development@s3dev.uk>',
             'name': 'utils4',
             'summary': 'A general utilities package for Python 3.7+.',
             'requires_dist': ['colorama'],
             'version': '1.7.0',
             'latest_version': '1.7.0'}


        Query the metadata which is *specific to a release*, from PyPI::

            >>> from ppklib import PyPIQuery

            >>> pquery = PyPIQuery.metadata(wheel='utils4-1.7.0-cp312-cp312-win_amd64.whl')

            >>> # Inspect the retrieved data.
            >>> pquery.data
            {'author': None,
             'author_email': 'The Developers <development@s3dev.uk>',
             'name': 'utils4',
             'summary': 'A general utilities package for Python 3.7+.',
             'requires_dist': ['colorama'],
             'version': '1.7.0',
             'yanked': False,
             'yanked_reason': None,
             'filename': 'utils4-1.7.0-cp312-cp312-win_amd64.whl',
             'md5_digest': 'c8e0b67399cedb52ade57a2d33f52fe6',
             'python_version': 'cp312',
             'packagetype': 'bdist_wheel',
             'requires_python': '>=3.7',
             'upload_time_iso_8601': '2025-01-04T17:13:14.409585Z',
             'vulnerabilities': [],
             'latest_version': '1.7.0'}


        Query the metadata which is *specific to a release*, from PyPI
        (for a project with reported vulnerabilities)::

            >>> from ppklib import PyPIQuery

            >>> wheel = 'numpy-1.20.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl'
            >>> pquery = PyPIQuery.metadata(wheel=wheel)

            >>> # Inspect the reported vulnerabilities. (Example details have been truncated.)
            >>> pquery.vulns
            [{'aliases': ['CVE-2021-33430'],
              'details': 'A Buffer Overflow vulnerability exists in NumPy 1.9.x in the ...',
              'fixed_in': ['1.21'],
              'id': 'GHSA-6p56-wp2h-9hxr',
              'link': 'https://osv.dev/vulnerability/GHSA-6p56-wp2h-9hxr',
              'source': 'osv',
              'summary': None,
              'withdrawn': None},
             {'aliases': ['CVE-2021-34141'],
              'details': 'Incomplete string comparison in the numpy.core component in ...',
              'fixed_in': ['1.22'],
              'id': 'GHSA-fpfv-jqm9-f5jm',
              'link': 'https://osv.dev/vulnerability/GHSA-fpfv-jqm9-f5jm',
              'source': 'osv',
              'summary': None,
              'withdrawn': None}]

    """

    @classmethod
    def metadata(cls,
                 name: str=None,
                 *,
                 version: str=None,
                 wheel: str=None) -> PyPIAPIObject | None:
        """Query a project's metadata.

        Args:
            name (str, optional): Name of the project to be queried.
                Defaults to None.
            version (str, optional): Return metadata specific to this
                version. Defaults to None.
            wheel (str, optional): Return release metadata specific to
                this wheel file. Defaults to None.

        .. tip::

            1) If only the ``name`` argument is provided, only the
               top-level metadata will be queried, for the *latest*
               version.

            2) If the ``name`` and ``version`` arguments are provided,
               only the top-level metadata will be queried, for the
               specific version.

            3) However, if *all three* parameters are provided (or the
               only the wheel filename), the version-specific release
               metadata will be returned. (**Preferred**)

               This is the preferred method because if only the wheel
               filename is provided, the package name and version are
               parsed from the filename - this enables a simple function
               call with only a single argument (the wheel filename).

        Returns:
            PyPIAPIObject | None : Object containing the project metadata
            from PyPI. On error, None is returned.

        """
        try:
            apio = PyPIAPIObject(name=name, version=version, wheel=wheel)
            apio.get_and_filter()
            return apio
        except Exception as err:
            ui.print_alert('\n[ERROR]: An error occurred while querying project metadata.\n')
            print(*traceback.format_exception(err), sep='\n')
        return None
