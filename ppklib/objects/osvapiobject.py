#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the object implementation for
            interacting with the `Open Source Vulnerabilities <osvweb_>`_
            (OSV) API.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:References:

            The following links provide the requirements (specification)
            on which this module's logic and API interactions are based:

                - `OSV API <osvapi_>`_

:Example:

            Create an instance of the object and query the API to obtain
            *version-specific* vulnerabilities::

                >>> from ppklib.objects.osvapiobject import OSVAPIObject

                >>> oapi = OSVAPIObject(name='numpy', version='1.20.0')
                >>> oapi.get()

                >>> # Inspect the raw JSON data.
                >>> oapi.rawjson
                {'not_shown': 'too_big'}


            Create an instance of the object and query the API to obtain
            *version-specific* vulnerabilities, **and** subset the raw
            API response to frequently used keys::

                >>> from ppklib.objects.osvapiobject import OSVAPIObject

                >>> oapi = OSVAPIObject(name='numpy', version='1.20.0')
                >>> oapi.get_and_filter()

                >>> # View the reported vulnerabilities.
                >>> oapi.vulns
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

                >>> # View the count of each severity class.
                >>> oapi.counts
                <SeverityCountsObject> C: 0, H: 0, M: 2, L: 0

            .. _osvapi: https://google.github.io/osv.dev/api/
            .. _osvweb: https://google.github.io/osv.dev/

"""
# pylint: disable=wrong-import-order

import os
import requests
import traceback
from utils4.user_interface import ui
# locals
try:  # nocover
    from ..libs.config import systemcfg as syscfg
    from ..libs.utilities import utilities as ppkutils
    from ..objects.severitycountsobject import SeverityCountsObject
except ImportError:
    from libs.config import systemcfg as syscfg
    from libs.utilities import utilities as ppkutils
    from objects.severitycountsobject import SeverityCountsObject


class OSVAPIObject:
    """Object designed for interacting with OSV's API.

    Args:
        name (str, optional): Name of the package to query. Providing
            only the name will return the *all* project-related
            vulnerabilities. For wheel-specific (release-specific)
            vulnerabilities, provide the ``version`` and/or ``wheel``
            arguments too. Defaults to None.
        version (str, optional): Query the vulnerabilities specific to
            this version; otherwise the vulnerabilities for *all*
            versions will be returned. Defaults to None.
        wheel (str, optional): Wheel filename. Providing *only* this
            argument will return version-specific vulnerability
            information. The project name and version will be parsed
            from the wheel filename. Defaults to None.

    .. tip:
        To retrieve release-specific vulnerabilities, provide the
        ``wheel`` filename argument only.

        The project name and version will be derived from the wheel
        filename.

    """

    __slots__ = (
                 '_counts',
                 '_name',
                 '_rawjson',
                 '_status_code',
                 '_version',
                 '_vulns',
                 '_wheel',
                )

    def __init__(self, name: str=None, version: str=None, wheel: str=None):
        """OSV API object class initialiser."""
        self._name = name           # \
        self._version = version     #  -- Class arguments
        self._wheel = wheel         # /
        self._counts = None         # Severity class counts.
        self._rawjson = {}          # Raw JSON reqponse from GET request.
        self._status_code = 0       # Status code returned by the response.
        self._vulns = []            # Processed (filtered) vulnerabilities.
        self._test_args()

    def __repr__(self) -> str:
        """String representation of the object."""
        if not self._version:
            a = f'{self.__class__.__name__}: {self._name}'
        else:
            a = f'{self.__class__.__name__}: {self._name} v{self._version}'
        if not self._rawjson:
            b = 'Data: None'
        elif all((self._rawjson, not self._vulns)):
            b = 'Data: Raw'
        elif all((self._rawjson, self._vulns)):
            b = 'Data: Vulnerabilities'
        else:
            b = 'Unknown'  # nocover  # Should be unreachable.
        return f'<{a} {b}>'

    @property
    def counts(self) -> SeverityCountsObject:
        """Accessor to the severity class counts."""
        return self._counts

    @property
    def name(self) -> str:
        """Accessor to the name of the target package."""
        return self._name

    @property
    def rawjson(self) -> dict:
        """Accessor to the raw JSON data returned by the API.

        This property returns the *complete* JSON response from the API.

        """
        return self._rawjson

    @property
    def status_code(self) -> int:
        """Accessor to the response's status code."""
        return self._status_code

    @property
    def version(self) -> str:
        """Accessor to the version number of the target package."""
        return self._version

    @property
    def vulns(self) -> list:
        """Accessor to the filtered vulnerabilities as a list of dicts.

        This property returns the *filtered* response from the API as a
        list of relatively flat dictionaries. This is to enable easy
        conversion to a ``pandas.Series`` or ``pandas.DataFrame``.

        If the full response is required, please use the :attr:`rawjson`
        property.

        """
        return self._vulns

    @property
    def wheel(self) -> str:
        """Accessor to the wheel's filename for the target package."""
        return self._wheel

    def get(self) -> bool:
        """Query the PyPI database using the JSON API.

        Use this method to populate the :attr:`_rawjson` attribute, which
        is accessed through the :attr:`rawjson` property.

        Returns:
            bool: True if the request succeeds, otherwise False.

        """
        try:
            return self._getrequest()
        except Exception as err:
            print(*traceback.format_exception(err), sep='\n')
        return False  # nocover

    def get_and_filter(self):
        """Query the OSV database using the API and filter the results.

        This method filters the full JSON response to create a
        list of (relatively) flattened dictionaries with the
        'frequently used'/'most descriptive' key/value pairs for the
        reported vulnerabilities. These are stored into the :attr:`vulns`
        property for access.

        The primary purpose for creating a flattened subset is to
        facilitate easy conversion to a ``pandas.Series`` or
        ``pandas.DataFrame``, as these can be created from a simple
        ``dict`` object.

        If the full response is required, please use the :attr:`rawjson`
        property.

        """
        try:
            if self.get():
                self._flatten_vulnerability_data()
                self._counts = SeverityCountsObject(vulns=self._vulns)
        except Exception as err:
            print(*traceback.format_exception(err), sep='\n')

    def _build_request(self) -> dict:
        """Build the GET request using the available arguments.

        Returns:
            dict: A dictionary containing the parameters required for a
            :func:`requests.get` request. Simply pass this dict into
            the function with double asterisks for unpacking.

        """
        if not self._version:
            req = {'url': syscfg['api']['osv']['url'], 'json': {'package': {'name': self._name,
                                                                            'ecosystem': 'PyPI'}}}
        else:
            req = {'url': syscfg['api']['osv']['url'], 'json': {'version': self._version,
                                                                'package': {'name': self._name,
                                                                            'ecosystem': 'PyPI'}}}
        req.update({'headers': syscfg['api']['osv']['headers']})
        return req

    def _flatten_vulnerability_data(self):
        """Filter the 'frequently used' vulnerability items into a dict.

        The result of the filter can be accessed via the :attr:`vulns`
        property.

        """
        if self._rawjson:
            for v in self._rawjson['vulns']:
                if 'database_specific' in v:
                    vulns = {}
                    for k in syscfg['api']['osv']['keys']['vulns']:
                        vulns[k] = v.get(k)
                    vulns['severity'] = v.get('database_specific').get('severity')
                    if 'severity' in v:
                        vulns['vectors'] = [{s.get('type'): s.get('score')} for s in v['severity']]
                self._vulns.append(vulns)

    # TODO: Move this to a generalised API class/module.
    #       Note this is a POST request whereas the PyPI API is a GET
    #       request.
    def _getrequest(self) -> bool:
        """Send the GET request to the API and store the response.

        If successful, the raw JSON response is stored into the
        :attr:`_rawjson` attribute of this class.

        Returns:
            bool: True if the response to the GET request is 200,
            otherwise False.

        """
        req = self._build_request()
        resp = requests.post(**req, timeout=3)
        self._status_code = resp.status_code
        if resp.status_code == 200:
            self._rawjson = resp.json()
            return True
        msg = f'\n[ERROR]: Request error {resp.status_code} ({resp.reason}) for "{self._name}"'
        msgv = f' v{self._version}.' if self._version else '.'
        ui.print_alert(msg + msgv)
        return False

    # TODO: Move this to a generalised API class/module.
    def _test_args(self) -> None:
        """Verify the appropriate arguments are provided.

        :Tasks:
            - Normalise the :attr:`name` attribute value.
            - If either the name or version are not provided, and the
              wheel filename is provided, the name and version are
              derived from the wheel filename.

        """
        if not any((self._name, self._wheel)):
            raise ValueError('At least a package name or wheel filename must be provided.')
        if self._name:
            self._name = ppkutils.normalise_name(name=self._name)
        # If the wheel is provided, derive name/version if not already provided.
        if all((not self._name or not self._version, self._wheel)):
            # Cannot test the file signature as only the basename is provided.
            if not any((self._wheel.endswith('.tar.gz'),
                        os.path.splitext(self._wheel)[1] == '.whl')):
                raise ValueError('The argument passed to \'wheel=\' must be a valid wheel or '
                                 'tar.gz source archive.')
            # .tar.gz files must be parsed differently (str.find returns -1 on failure).
            if ( idx := self._wheel.find('.tar.gz') ) > 0:
                self._name, self._version = self._wheel[:idx].rsplit('-', maxsplit=1)
            else:
                self._name, self._version, *_ = self._wheel.split('-')
