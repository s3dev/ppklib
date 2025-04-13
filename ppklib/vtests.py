#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the vulnerability tests to the project.

            Any wheel which is downloaded from PyPI is subject to the
            following tests, as contained in this module:

                - MD5 checksum verification
                - Snyk security vulnerability checks

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  This module is designed to be as self-contained as practical.

            All tests should be contained in this module as individual
            methods, while following the DRY paragigm to the extent
            possible.

"""
# pylint: disable=import-error

import os
import requests
from bs4 import BeautifulSoup
from utils4.crypto import crypto
# locals
try:
    from .utilities import utilities as ppkutils
except ImportError:
    from ppklib.utilities import utilities as ppkutils


class Tests:
    """Wrapper class for the tests to be carried out on the packages."""
    # The **kwargs are used as a blackhole for unused arguments.
    # pylint: disable=unused-argument

    @staticmethod
    def md5(fpath: str, name: str, version: str, **kwargs) -> tuple:
        """Perform an MD5 check against the PyPI database to verify
        integrity.

        Args:
            fpath (str): Complete path to the package (wheel) to be
                verified.
            name (str): Package name.
            version (str): Package version to be tested.

        :Keyword Arguments:
            None

        Returns:
            tuple: A tuple containig the verification flag. True if the
            MD5 hashes match, otherwise False.

            The second element of the tuple is empty, but used for
            consistency in test return values.

        """
        md5p = None
        fname = os.path.basename(fpath)
        data = ppkutils.query_pypi(pkg=name)
        # Iterate until the specific file is found.
        for record in data['releases'][version]:
            if record['filename'] == fname:
                md5p = record['digests']['md5']
                break  # Stop after file is found.
        # Generate own md5 and verify.
        md5c = crypto.checksum_md5(path=fpath)
        if md5c == md5p:
            return (True,)
        return (False,)

    @staticmethod
    def snyk(name: str, version: str, verbose: bool=True, **kwargs) -> tuple:
        """Use Snyk.io to test for reported vulnerabilities.

        If a package has reported direct vulnerabilities, these are
        captured and reported to the terminal at the end of processing.

        A package is considered 'passing' if no 'Critical' and 'High'
        vulnerabilities have been reported.

        Args:
            name (str): Package name.
            version (str): Package version to be tested.
            verbose (bool, optional): Print all reported vulnerabilities to
                the terminal on test completion. Defaults to True.

        :Keyword Arguments:
            None

        Returns:
            tuple: A tuple containing the verification flag, and
            supporting data.

            True if there are no reported 'Critical' or 'High'
            vulverabilities, otherwise False. The trailing elements are
            the number of vulnerabilities found in each category, of
            descending severity (i.e. C, H, M, L).

            If the ``verbose`` flag is ``True``, the known vulnerabilities
            are reported to the terminal on test completion.

        """
        # pylint: disable=line-too-long
        # pylint: disable=too-many-locals
        # Force failure -- DEV ONLY.
        # name = 'numpy'
        # version = '1.8.0'
        # --|
        url = f'https://security.snyk.io/package/pip/{name}'
        with requests.get(url, timeout=3) as r:
            soup = BeautifulSoup(r.text, 'html.parser')
        # Find the table and rows.
        div = soup.find('div', attrs={'class': 'package-versions-table__table'})
        rows = div.findAll('tr', attrs={'class': 'table__row'})  # Changed in v0.3.0
        # Skip header row.
        rows.pop(0)
        # Initialise the direct vulnerabilities set.
        dvset = set()
        vuln_n = []
        for row in rows:
            # Search for specific version.
            if row.find('a').attrs['href'].endswith(version):
                td = row.findAll('td')
                if td:
                    # Extract relevent values.
                    vuln_n = list(map(lambda x: int(x.text), td[2].findAll('div')))  # Changed in v0.3.0
                    # If any direct vulnerabilities are found, report them.
                    if any(vuln_n):
                        with requests.get(f'{url}/{version}', timeout=10) as r:
                            soup = BeautifulSoup(r.text, 'html.parser')
                        # soup = soupv  # Read from file -- DEV ONLY.
                        div = soup.find('div', attrs={'class': 'vulns-table__wrapper'})
                        rows = div.findAll('tr', attrs={'class': 'table__row'})  # Changed in v0.3.0
                        rows.pop(0)  # Skip header row.
                        for row in rows:
                            vlabel = row.find('abbr', attrs={'class': 'severity__text'}).text.strip()  # Changed in v0.3.0
                            vtitle = row.find('a').text.strip()
                            vvers = row.find('div', attrs={'class': 'vulnerable-versions'}).text.strip()
                            dvset.add((vlabel, vtitle, vvers))
                break  # Stop after version is found.
        # End of processing summary.
        if verbose and dvset:
            tmpl = '{:10}{:40}{:25}'
            print(f'\n{name} v{version} has the following reported direct vulnerabilities:',
                  '',
                  tmpl.format('Severity', 'Title', 'Versions'),
                  tmpl.format('--------', '-----', '--------'),
                  sep='\n')
            for i in dvset:
                print(tmpl.format(*i))
            print()
        if not any(vuln_n):
            print(f'{name} v{version} has no reported direct vulnerabilities.')
        return (not any(vuln_n[:2]), *vuln_n)  # Pass --> No C(ritical) or H(igh) vulnerabilities.
