#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the functionality for reading and
            importing the ``config.toml`` file to the project.

:Platform:  Linux/Windows | Python 3.10+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  If the version of Python is 3.11+, the ``tomllib`` builtin
            is used to load the config file. Otherwise, the third-party
            ``toml`` library is used. If ``toml`` is not installed, the
            user is notified the library must be installed, and the
            program is exited.

"""
# pylint: disable=import-error

import os
import sys
from utils4.user_interface import ui


# Check Python version. The tomllib is only available for >= 3.11.
_GEQ311 = sys.version_info >= (3, 11)
if _GEQ311:
    import tomllib
else:
    try:  # nocover
        import toml
    except ImportError:
        ui.print_warning('As a Python version less than 3.11 is being used, '
                         'the toml library must be installed.')
        sys.exit(1)


class Config:
    """General project configuration wrapper class.

    Note:
        This class is used to simply read and provide access to the
        settings defined in the ``config.toml`` file.

        All configuration keys are to be set in the ``config.toml`` file,
        not in this module.

    """

    _DIR_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    _DIR_LIBS = os.path.join(_DIR_ROOT, 'libs')

    def __init__(self):
        """Configuration class initialiser."""
        self._fullcfg = None
        self._projcfg = None
        self._syscfg = None
        self._load_config()

    @property
    def config(self):
        """Public accessor to all configuration items."""
        return self._fullcfg

    @property
    def projectcfg(self):
        """Public accessor to the project configuration keys."""
        return self._projcfg

    @property
    def systemcfg(self):
        """Public accessor to system configuration items."""
        return self._syscfg

    def _load_config(self):
        """Load the config TOML file into memory.

        This method is called on class instantiation.

        If using Python 3.11+, the builtin ``tomllib`` library is used
        to read the config file. Otherwise, the third-party ``toml``
        library is used.

        """
        path = os.path.join(self._DIR_LIBS, 'config.toml')
        if _GEQ311:
            with open(path, 'rb') as f:
                self._fullcfg = tomllib.load(f)
        else:  # nocover
            self._fullcfg = toml.load(path)
        self._projcfg = self._fullcfg.get('project')
        self._syscfg = self._fullcfg.get('system')


_config = Config()
config = _config.config
projectcfg = _config.projectcfg
systemcfg = _config.systemcfg
