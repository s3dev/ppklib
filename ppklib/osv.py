#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides functionality for collecting
            vulnerability metrics from
            `Open Source Vulnerabilities <osvweb_>`_ (OSV); specifically,
            through the OSV API.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:References:

            The following links provide the requirements (specification)
            on which this module's logic and API interactions are based:

                - `OSV API <osvapi_>`_

:Comments:  n/a

            .. _osvweb: https://google.github.io/osv.dev/
            .. _osvapi: https://google.github.io/osv.dev/api/

"""

import traceback
from utils4.user_interface import ui
# locals
try:
    from .objects.osvapiobject import OSVAPIObject
except ImportError:
    from objects.osvapiobject import OSVAPIObject


class OSVQuery:
    """Class for querying the OSV API.

    :Examples:

        Query a project's vulnerabilities via the OSV API, for a
        specific version::

            >>> from ppklib import OSVQuery

            >>> oquery = OSVQuery.vulnerabilities(name='numpy',
                                                  version='1.20.0')

            >>> # Inspect the retrieved vulnerabilities.
            >>> oquery.vulns
            [{'id': 'GHSA-6p56-wp2h-9hxr',
              'summary': 'NumPy Buffer Overflow (Disputed)',
              'aliases': ['CVE-2021-33430', 'PYSEC-2021-854'],
              'published': '2022-01-07T00:09:39Z',
              'modified': '2024-09-26T15:01:21.525444Z',
              'severity': 'MODERATE',
              'vectors': [{'CVSS_V3': 'CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:H'},
               {'CVSS_V4': 'CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N'}]},
             {'id': 'GHSA-fpfv-jqm9-f5jm',
              'summary': 'Incorrect Comparison in NumPy',
              'aliases': ['CVE-2021-34141', 'PYSEC-2021-855'],
              'published': '2021-12-18T00:00:41Z',
              'modified': '2023-11-08T04:06:07.388275Z',
              'severity': 'MODERATE',
              'vectors': [{'CVSS_V3': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L'}]}]

    """

    @classmethod
    def vulnerabilities(cls,
                        name: str=None,
                        *,
                        version: str=None,
                        wheel: str=None) -> OSVAPIObject | None:
        """Query a project's vulnerabilities.

        Args:
            name (str, optional): Name of the project to be queried.
                Defaults to None.
            version (str, optional): Return vulnerabilities specific to
                this version. Defaults to None.
            wheel (str, optional): Return version specific
                vulnerabilities. Passing only this argument performs the
                same query as providing both the ``name`` and ``version``
                arguments. Defaults to None.

        .. tip::

            1) If only the ``name`` argument is provided, all
               vulnerabilities for the project are queried. *However*, as
               pagination is *not* automatically implemented, the actual
               response may be more than what is returned on the first
               page.

               It is recommended to narrow the search to a specific
               version. Keep reading ...

            2) If the ``name`` and ``version`` arguments are provided,
               only the vulnerabilities specific to this version are
               returned.

            3) If the ``wheel`` argument is used, this performs the same
               query as providing both the ``name`` and ``version``
               arguments. (**Preferred**)

               This is the preferred method because if only the wheel
               filename is provided, the package name and version are
               parsed from the filename - this enables a simple function
               call with only a single argument (the wheel filename).

        Returns:
            OSVAPIObject | None : Object containing the project
            vulnerability details, per OSV. On error, None is returned.

        """
        try:
            oapi = OSVAPIObject(name=name, version=version, wheel=wheel)
            oapi.get_and_filter()
            return oapi
        except Exception as err:
            ui.print_alert('\n[ERROR]: An error occurred while querying project vulnerabilities.\n')
            print(*traceback.format_exception(err), sep='\n')
        return None
