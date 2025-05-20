#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the object implementation for the
            ``SeverityCounts`` object.

            This object is used as a storage container and accessor to
            the number of vulnerabilities for each severity class, for a
            given project or release.

:Platform:  Linux/Windows | Python 3.8+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

"""


class SeverityCountsObject:
    """Container and accessor class for vulnerability severity counts.

    Args:
        vulns (list): A list of dictionary objects containing the
            vulnerabilities for a given project or release. Note, this
            is expected to be a ``list`` of ``dict`` objects, each
            containing *at least* a ``'severity'`` key. The case of the
            severity string value does not matter.

            Example expected *minimal* ``vulns`` structure::

                [
                 {'severity': 'Low'},
                 ...,
                 {'severity': 'High'}
                ]

            Expected severity string values:

                - Low
                - Moderate or Medium
                - High
                - Critical

    """

    __slots__ = ('_c', '_h', '_l', '_m')

    def __init__(self, vulns: list):
        """Severity counts object initialiser."""
        self._c = 0  # Critical
        self._h = 0  # High
        self._l = 0  # Low
        self._m = 0  # Moderate
        self._set(vulns=vulns)

    def __iter__(self):
        """Provide an iterable type.

        This method is used for cases like::

            tuple(SeverityCountsObject)

        Yields:
            int: Severity counts in *descending* severity order.

        """
        for i in ('critical', 'high', 'moderate', 'low'):
            yield getattr(self, i)

    def __repr__(self) -> str:
        """String representation of the object's contents."""
        name = self.__class__.__name__
        s = f'<{name}> C: {self._c}, H: {self._h}, M: {self._m}, L: {self._l} (Total: {self.total})'
        return s

    #
    # These are ordered by severity, so they appear in a logical order.
    #

    @property
    def low(self) -> int:
        """Accessor to the number of LOW severity class entries."""
        return self._l

    @property
    def moderate(self) -> int:
        """Accessor to the number of MODERATE severity class entries.

        This accessor applies to both the MODERATE and MEDIUM classes.

        """
        return self._m

    @property
    def high(self) -> int:
        """Accessor to the number of HIGH severity class entries."""
        return self._h

    @property
    def critical(self) -> int:
        """Accessor to the number of CRITICAL severity class entries."""
        return self._c

    @property
    def total(self) -> int:
        """Accessor to the TOTAL number of vulnerabilities for a release."""
        return sum((self._l, self._m, self._h, self._c))

    def _set(self, vulns: list) -> None:
        """Set the vulnerability counts based on the input data.

        Args:
            vulns (list): The ``vulns`` list passed into the class.

        """
        for v in vulns:
            if v.get('severity', '').lower() in {'low'}:
                self._l += 1
            elif v.get('severity', '').lower() in {'moderate', 'medium'}:
                self._m += 1
            elif v.get('severity', '').lower() in {'high'}:
                self._h += 1
            elif v.get('severity', '').lower() in {'critical'}:
                self._c += 1
