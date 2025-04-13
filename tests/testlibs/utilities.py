#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides shared utilities, which are dedicated
            to unit testing.

:Platform:  Linux/Windows | Python 3.7+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:
    Example code use::

        from testlibs.utilities import utilities

"""
# pylint: disable=import-error
# pylint: disable=wrong-import-order

import numpy as np
import pandas as pd
from base import TestBase
from typing import Union


class Utilities(TestBase):
    """General testing utility methods class."""

    def assert_equal_dataframe(self, df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
        """Generalised test runner for testing the equality of two DataFrames.

        :Assertion:

            - ``df1.equals(df2)``

        Args:
            df1 (pd.DataFrame): Source data DataFrame.
            df2 (pd.DataFrame): Test data DataFrame.

        """
        self.assertTrue(df1.equals(df2))

    def assert_false(self, expected: Union[str, int], test: Union[str, int], msg: str):
        """Generalised test runner for Python strings and ints.

        :Assertion:

            - ``(expected == test) is False``

        Args:
            expected (Union[str, int]): Expected value.
            test (Union[str, int]): Result of the test to be tested against
                the expected value.
            msg (str): Template string into which the expected and actual
                values can be displayed.

        """
        self.assertFalse(expected == test, msg.format(expected, test))

    def assert_true(self, expected: Union[str, int], test: Union[str, int], msg: str):
        """Generalised test runner for Python strings and ints.

        :Assertion:

            - ``(expected == test) is True``

        Args:
            expected (Union[str, int]): Expected value.
            test (Union[str, int]): Result of the test to be tested against
                the expected value.
            msg (str): Template string into which the expected and actual
                values can be displayed.

        """
        self.assertTrue(expected == test, msg.format(expected, test))

    def assert_true_array(self, expected: np.ndarray, test: np.ndarray, msg: str):
        """Generalised test runner for numpy arrays.

        :Assertion:

            - ``(expected == test).all() is True``

        Args:
            expected (np.ndarray): Expected array contents.
            test (np.ndarray): Result of the test, to be tested against
                the expected array.
            msg (str): Template string into which the expected and actual
                values can be displayed.

        """
        self.assertTrue((expected == test).all(), msg.format(expected[:5], test[:5]))

    def assert_true_pyiter(self, expected: list, test: list, msg: str):
        """Generalised test runner for Python lists or iterable objects.

        :Assertion:

            - ``(expected == test) is True``

        Args:
            expected (list): Expected list contents.
            test (list): Result of the test, to be tested against
                the expected list.
            msg (str): Template string into which the expected and actual
                values can be displayed.

        """
        self.assertTrue(expected == test, msg.format(expected, test))


utilities = Utilities()
