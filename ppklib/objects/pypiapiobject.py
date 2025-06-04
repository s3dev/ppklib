#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the object implementation for
            interacting with PyPI's JSON API.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:References:

            The following links provide the requirements (specification)
            on which this module's logic and API interactions are based:

                - `PyPI Index API <indexapi_>`_
                - `PyPI JSON API <jsonapi_>`_

:Example:

            Create an instance of the object and query the API to obtain
            *release-specific* metadata::

                >>> from ppklib.objects.jsonapiobject import PyPIAPIObject

                >>> papi = PyPIAPIObject(name='utils4',
                                         version='1.7.0',
                                         wheel='utils4-1.7.0-cp312-cp312-win_amd64.whl')
                >>> papi.get_and_filter()

                >>> # Inspect the flattened data.
                >>> papi.data
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

            .. _indexapi: https://docs.pypi.org/api/index-api/
            .. _jsonapi: https://docs.pypi.org/api/json/

"""
# pylint: disable=wrong-import-order

import os
import requests
import traceback
from datetime import datetime as dt
from utils4.user_interface import ui
# locals
try:  # nocover
    from ..libs.config import systemcfg as syscfg
    from ..libs.utilities import utilities as ppkutils
except ImportError:
    from libs.config import systemcfg as syscfg
    from libs.utilities import utilities as ppkutils


class PyPIAPIObject:
    """Object designed for interacting with PyPI's JSON API.

    Args:
        name (str, optional): Name of the package to query. Providing
            only the name will return the *latest* project-based
            metadata. For wheel-specific (release-specific) metadata,
            provide the ``version`` and/or ``wheel`` arguments too.
            Defaults to None.
        version (str, optional): Query the metadata specific to this
            version; otherwise the metadata for the *latest* version
            will be returned. Defaults to None.
        wheel (str, optional): Wheel filename. Providing *only* this
            argument will return version-specific release information.
            The project name and version will be parsed from the wheel
            filename. Defaults to None.

    .. tip:
        To retrieve release-specific metadata, provide the ``wheel``
        filename argument only.

        The project name and version will be derived from the wheel
        filename.

    """

    __slots__ = (
                 '_data',
                 '_name',
                 '_rawjson',
                 '_status_code',
                 '_version',
                 '_wheel',
                )

    def __init__(self, name: str=None, version: str=None, wheel: str=None):
        """PyPI API object class initialiser."""
        self._name = name           # \
        self._version = version     #  -- Class arguments
        self._wheel = wheel         # /
        self._data = {}             # Processed (filtered) JSON data.
        self._rawjson = {}          # Raw JSON reqponse from GET request.
        self._status_code = 0       # Status code returned by the response.
        self._test_args()

    def __repr__(self) -> str:
        """String representation of the object."""
        if not self._version:
            a = f'{self.__class__.__name__}: {self._name}'
        else:
            a = f'{self.__class__.__name__}: {self._name} v{self._version}'
        if not self._rawjson:
            b = 'Data: None'
        elif all((self._rawjson, not self._data)):
            b = 'Data: Raw'
        elif all((self._rawjson, self._data, not self._wheel)):
            b = 'Data: Metadata'
        else:
            b = 'Data: Metadata (release)'
        return f'<{a} {b}>'

    @property
    def data(self) -> dict:
        """Accessor to the filtered JSON response as a *flat* dictionary.

        This property returns the *filtered* response from the JSON API
        as a *flattened* dictionary. This is to enable easy conversion
        to a ``pandas.Series`` or ``pandas.DataFrame``.

        """
        return self._data

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
        """Accessor to the vulnerabilities as listed by PyPI.

        Specifically, this is an accessor to the ``'vulnerabilities'``
        key of the :attr:`data` property, which is a *subset* of the API
        response.

        If the full response is required, please use the :attr:`rawjson`
        property.

        Note:
            Vulnerabilities are only available if the ``wheel`` argument
            is used on instantiation, as the ``wheel`` argument is used
            to query a specific release from PyPI.

        """
        return self._data.get('vulnerabilities')

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
        """Query the PyPI database using the JSON API and filter the results.

        This method filters the full response to create a *flattened*
        dictionary with the 'frequently used'/'most descriptive'
        key/value pairs.

        The primary purpose for creating a flattened subset is to
        facilitate easy conversion to a ``pandas.Series`` or
        ``pandas.DataFrame``, as these can be created from a simple
        ``dict`` object.

        """
        try:
            if self.get():
                self._extract_project_metadata()
                self._extract_release_metadata()
                self._get_latest_version()
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
            url = syscfg['api']['pypi']['url'].format(name=self._name)
        else:
            url = syscfg['api']['pypi']['urlv'].format(name=self._name, version=self._version)
        return {'url': url, 'headers': syscfg['api']['pypi']['headers']}

    def _extract_release_metadata(self) -> None:
        """Extract release-specific metadata from the response.

        This method extracts release-specific metadata from the
        ``['urls']`` key and therefore both the ``version`` *and*
        ``wheel`` arguments must be provided. If these are missing, this
        method is not executed.

        Note:
            The extracted keys from the ``'urls'`` key of the raw JSON
            are defined in ``libs/config.toml``.

        """
        data = {}
        if all((self._version, self._wheel)):
            keys = syscfg['api']['pypi']['keys']['release']
            for r in self._rawjson['urls']:
                if r['filename'] == self._wheel:
                    data = {k: r[k] for k in keys}
                    break  # Can only refer to a single wheel. Once found, get out.
            data['vulnerabilities'] = self._rawjson['vulnerabilities']
            # A TypeError is thrown if the fromisoformat arg is not a str.
            if (upload := data.get('upload_time_iso_8601')) and isinstance(upload, str):
                data['upload_time_iso_8601'] = dt.fromisoformat(upload)
        self._data.update(data)

    def _extract_project_metadata(self) -> None:
        """Extract project metadata from the response.

        This method only extracts metadata from the ``['info']`` key and
        is therefore *only* project (not release) data.

        Note:
            The extracted keys from the ``'info'`` key of the raw JSON
            are defined in ``libs/config.toml``.

        """
        keys = syscfg['api']['pypi']['keys']['project']
        data = {k: self._rawjson['info'][k] for k in keys}
        # ???: Get license info.
        #      This may need some more thought later as some packages
        #      (.e.g pandas, numpy) display the full license rather than
        #      only the type.
        data['license'] = (self._rawjson['info']['license_expression']
                           or self._rawjson['info']['license'])
        if data['license'] and len(data['license']) > 10:
            data['license'] = 'Full license displayed'
        self._data = data

    def _get_latest_version(self) -> None:
        """Query to get the latest version of the package.

        Note:
            This must be a separate request as the ``version`` key lists
            the version of the queried package, which differs if the
            version parameter of the API is provided. Therefore, this
            query is run *without* a specified version to ensure the
            latest version is obtained.

        """
        obj = PyPIAPIObject(name=self._name, version='')  # Explicitly exclude the version.
        obj.get()
        self._data.update({'latest_version': obj.rawjson['info']['version']})

    def _getrequest(self) -> bool:
        """Send the GET request to the API and store the response.

        If successful, the raw JSON response is stored into the
        :attr:`_rawjson` attribute of this class.

        Returns:
            bool: True if the response to the GET request is 200,
            otherwise False.

        """
        req = self._build_request()
        resp = requests.get(**req, timeout=3)
        self._status_code = resp.status_code
        if resp.status_code == 200:
            self._rawjson = resp.json()
            return True
        msg = f'\n[ERROR]: Request error {resp.status_code} ({resp.reason}) for "{self._name}"'
        msgv = f' v{self._version}.' if self._version else '.'
        ui.print_alert(msg + msgv)
        return False

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
