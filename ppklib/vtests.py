#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the vulnerability tests to the project.

            Any wheel which is downloaded from PyPI is subject to the
            following tests, as contained in this module:

                - MD5 checksum verification
                - OSV security vulnerability checks
                - Snyk security vulnerability checks

:Platform:  Linux/Windows | Python 3.6+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  This module is designed to be as self-contained as practical.

            All tests should be contained in this module as individual
            methods, while following the DRY paradigm to the extent
            possible.

"""
# pylint: disable=import-error

import os
import requests
from bs4 import BeautifulSoup
from utils4.crypto import crypto
# locals
try:
    from .osv import OSVQuery
    from .pypi import PyPIQuery
except ImportError:
    from osv import OSVQuery
    from pypi import PyPIQuery


class VTests:
    """Wrapper class for the vulnerability tests.

    :Usage:
        For specific usage examples, please refer to the docstrings for
        the following test methods:

            - :meth:`md5`
            - :meth:`osv`
            - :meth:`snyk`

    """

    # The **kwargs arguments are used as a blackhole for unused arguments
    # in efforts to keep the function signatures (and call formats) as
    # consistent as practical.
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

        :Example:

            Perform an MD5 check on a specific wheel::

                >>> from ppklib.vtests import VTests

                >>> tst = VTests.md5(fpath='path/to/ppklib-0.1.0-py3-none-any.whl',
                                     name='ppklib',
                                     version='0.1.0')

                # Check the result of the test; True == pass
                >>> tst
                (True,)

        Returns:
            tuple: A tuple containing the verification flag. True if the
            MD5 hashes match, otherwise False.

            The second element of the tuple is empty, but used for
            consistency in test return values.

        """
        md5p = None
        meta = PyPIQuery.metadata(wheel=os.path.basename(fpath))
        if meta:
            md5p = meta.data.get('md5_digest')
            # Generate own md5 and verify.
            md5c = crypto.checksum_md5(path=fpath)
            if md5c == md5p:
                return (True,)
        return (False,)  # nocover  # Cannot force a fail in testing.

    @staticmethod
    def osv(*, fpath: str='', name: str='', version: str='', verbose: bool=True, **kwargs) -> tuple:
        """Query the OSV database for any reported vulnerabilities.

        Args:
            fpath (str, optional): Complete path to the package (wheel) to be
                verified. Defaults to ''.
            name (str, optional): Package name. Defaults to ''.
            version (str, optional): Package version to be tested. Defaults to ''.
            verbose (bool, optional): Print all reported vulnerabilities
                to the terminal on test completion. Defaults to True.

        :Keyword Arguments:
            None

        :Example:

            Check the OSV vulnerability database for any reported
            vulnerabilities, for a library::

                >>> from ppklib.vtests import VTests

                >>> tst = VTests.osv(fpath='path/to/ppklib-0.1.0-py3-none-any.whl',
                                     name='ppklib',
                                     version='0.1.0')

                # Check the result of the test; True == pass
                >>> tst
                (True,0, 0, 0, 0)


            Check the OSV vulnerability database for any reported
            vulnerabilities, for a library *with* vulnerabilities::

                >>> from ppklib.vtests import VTests

                >>> tst = VTests.osv(name='numpy', version='1.13.1')

                numpy v1.13.1 has the following reported direct vulnerabilities, per OSV:

                Severity  Title                                   Alias
                --------  -----                                   -----
                HIGH      NumPy NULL Pointer Dereference          CVE-2021-41495
                MODERATE  NumPy Buffer Overflow (Disputed)        CVE-2021-33430
                CRITICAL  Numpy Deserialization of Untrusted Data CVE-2019-6446
                MODERATE  Buffer Copy without Checking Size of Input in NumPyCVE-2021-41496
                MODERATE  Incorrect Comparison in NumPy           CVE-2021-34141
                HIGH      Numpy missing input validation          CVE-2017-12852
                HIGH      Numpy missing input validation          CVE-2017-12852
                HIGH      Numpy missing input validation          CVE-2017-12852
                HIGH      Numpy missing input validation          CVE-2017-12852
                HIGH      Numpy missing input validation          CVE-2017-12852

                # Check the result of the test.
                >>> tst
                (False, 1, 6, 3, 0)

        Returns:
            tuple: A tuple containing the verification flag, and
            supporting data.

            True if there are no reported 'Critical' or 'High'
            vulnerabilities, otherwise False. The trailing elements are
            the number of vulnerabilities found in each category, of
            descending severity (i.e. C, H, M, L).

            If the ``verbose`` flag is ``True``, the known
            vulnerabilities are reported to the terminal on test
            completion.

        """
        # pylint: disable=line-too-long
        oquery = OSVQuery.vulnerabilities(name=name, version=version, wheel=os.path.basename(fpath))
        counts = tuple(oquery.counts)
        # End of processing summary.
        if verbose and oquery.vulns:
            tmpl = '{:10}{:39} {:25}'
            print(f'\n{name} v{version} has the following reported direct vulnerabilities, per OSV:',
                  '',
                  tmpl.format('Severity', 'Title', 'Alias'),
                  tmpl.format('--------', '-----', '-----'),
                  sep='\n')
            for v in oquery.vulns:
                i = (v['severity'], v['summary'], v['aliases'][0])
                print(tmpl.format(*i))
            print()
        if not any(oquery.vulns):
            print(f'{name} v{version} has no reported direct vulnerabilities, per OSV')
        return (not any(counts[:2]), *counts)  # Pass --> No C(ritical) or H(igh) vulnerabilities.

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

        :Examples:

            Check the Snyk vulnerability database for any reported
            vulnerabilities::

                >>> from ppklib.vtests import VTests

                >>> tst = VTests.snyk(name='utils4',
                                      version='1.5.0',
                                      verbose=False)

                utils4 v1.5.0 has no reported direct vulnerabilities.

                # Check the result of the test.
                >>> tst
                (True, 0, 0, 0, 0)


            Check the Snyk vulnerability database for any reported
            vulnerabilities, for a library *with* vulnerabilities::

                >>> from ppklib.vtests import VTests

                >>> tst = VTests.snyk(name='numpy',
                                      version='1.13.1',
                                      verbose=True)

                numpy v1.13.1 has the following reported direct vulnerabilities:

                Severity  Title                                   Versions
                --------  -----                                   --------
                L         Buffer Overflow                         [,1.21.0rc1)
                L         Denial of Service (DoS)                 [,1.22.0rc1)
                H         Denial of Service (DoS)                 [,1.13.3)
                L         NULL Pointer Dereference                [0,1.22.2)
                C         Arbitrary Code Execution                [0,1.16.3)
                L         Buffer Overflow                         [,1.22.0)

                # Check the result of the test.
                >>> tst
                (False, 1, 1, 0, 4)

        Returns:
            tuple: A tuple containing the verification flag, and
            supporting data.

            True if there are no reported 'Critical' or 'High'
            vulnerabilities, otherwise False. The trailing elements are
            the number of vulnerabilities found in each category, of
            descending severity (i.e. C, H, M, L).

            If the ``verbose`` flag is ``True``, the known
            vulnerabilities are reported to the terminal on test
            completion.

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
        rows = div.find_all('tr', attrs={'class': 'table__row'})  # Changed in v0.3.0
        # Skip header row.
        rows.pop(0)
        # Initialise the direct vulnerabilities set.
        dvset = set()
        vuln_n = []
        for row in rows:
            # Search for specific version.
            if row.find('a').attrs['href'].endswith(version):
                td = row.find_all('td')
                if td:
                    # Extract relevent values.
                    vuln_n = list(map(lambda x: int(x.text), td[2].find_all('div')))  # Changed in ppk v0.3.0
                    # If any direct vulnerabilities are found, report them.
                    if any(vuln_n):
                        with requests.get(f'{url}/{version}', timeout=10) as r:
                            soup = BeautifulSoup(r.text, 'html.parser')
                        # soup = soupv  # Read from file -- DEV ONLY.
                        div = soup.find('div', attrs={'class': 'vulns-table__wrapper'})
                        rows = div.find_all('tr', attrs={'class': 'table__row'})  # Changed in ppk v0.3.0
                        rows.pop(0)  # Skip header row.
                        for row in rows:
                            vlabel = row.find('abbr', attrs={'class': 'severity__text'}).text.strip()  # Changed in v0.3.0
                            vtitle = row.find('a').text.strip()
                            vvers = row.find('div', attrs={'class': 'vulnerable-versions'}).text.strip()
                            dvset.add((vlabel, vtitle, vvers))
                break  # Stop after version is found.
        # End of processing summary.
        if verbose and dvset:
            tmpl = '{:10}{:39} {:25}'
            print(f'\n{name} v{version} has the following reported direct vulnerabilities, per Snyk:',
                  '',
                  tmpl.format('Severity', 'Title', 'Versions'),
                  tmpl.format('--------', '-----', '--------'),
                  sep='\n')
            for i in dvset:
                print(tmpl.format(*i))
            print()
        if not any(vuln_n):
            print(f'{name} v{version} has no reported direct vulnerabilities, per Snyk')
        return (not any(vuln_n[:2]), *vuln_n)  # Pass --> No C(ritical) or H(igh) vulnerabilities.
