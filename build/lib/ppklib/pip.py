#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   This module provides the functionality related to calls to
            ``pip``.

:Platform:  Linux/Windows | Python 3.10+
:Developer: J Berendt
:Email:     development@s3dev.uk

:Comments:  n/a

:Example:

            Download pandas::

                >>> from ppklib.pip import Download

                >>> pipdl = Download('pandas')
                >>> pipdl.get()

                # Display the path to the downloaded target package.
                >>> pipdl.pkgpath

                # Optional cleanup after the wheels are no longer needed.
                >>> pipdl.cleanup()


            Download pandas version 2.2.3 for Windows and Python 3.13
            into a specified download directory::

                >>> from ppklib.pip import Download

                >>> pipdl = Download('pandas',
                                     version='2.2.3',
                                     args={'platform': 'win_amd64', 'python_version': '313'},
                                     tmpdir='/tmp/c0ff33')
                >>> pipdl.get()

                # Display the path to the downloaded target package.
                >>> pipdl.pkgpath

                # Optional cleanup after the wheels are no longer needed.
                >>> pipdl.cleanup()

"""

import os
import re
import sys
import subprocess as sp
import tempfile
import traceback
from argparse import Namespace
from glob import glob
from utils4.user_interface import ui
# locals
try:
    from .libs.utilities import utilities as ppkutils
except ImportError:
    from libs.utilities import utilities as ppkutils


class Download:
    """Processing related to the ``pip download`` command.

    Args:
        name (str): Name of the target library to be downloaded.
        version (str, optional): Specific version of the target library
            to be downloaded. If None, the latest version will be
            downloaded. Defaults to None.
        args (dict | Namespace, optional): A dict or the ``Namespace``
            object directly from the ``ppk`` argument parser. This will
            contain all the parameters required for the download.
            Generally, these will match ``pip``'s CLI arguments which
            are implemented in this library, with the hyphens converted
            to underscores. For example: pip's ``--python-version`` is
            ``python_version``. Defaults to None.
        reqfile (str, optional): Full path to the requirements.txt file,
            if applicable. If using a requirements file, pass ``None``
            to the ``name`` argument. Defaults to None.
        tmpdir (str, optional): Full path to the temp (download)
            directory. If None, a temp directory is automatically
            created. Defaults to None.

    """

    def __init__(self,
                 name: str,
                 *,
                 version: str=None,
                 args: dict | Namespace=None,
                 reqfile: str=None,
                 tmpdir: str=None):
        """Download class initialiser."""
        self._name = ppkutils.normalise_name(name=name)
        self._version = version
        self._args = args.__dict__ if isinstance(args, Namespace) else args or {}
        self._reqfile = reqfile
        self._tmpdir = None     # TemporaryDirectory object
        self._tmpdirname = ''
        self._pkg = None        # Filename of the downloaded target package.
        self._set_tmpdir_name(name=tmpdir)

    @property
    def pkgpath(self) -> str | None:
        """Accessor to the full path of the downloaded target package.

        Returns:
            str | None: The full path to the downloaded target package if
            downloaded successfully, otherwise None.

        """
        if self._pkg:
            return os.path.join(self._tmpdirname, self._pkg)
        return None

    def cleanup(self) -> None:
        """Remove the temporary directory and all downloaded files.

        Note:
            Cleanup is only called automatically on pip error. Otherwise,
            it's the user's (or caller's) decision to call for a
            cleanup.

        """
        self._cleanup()

    def get(self) -> str | None:
        """Collect the specified package and version (if provided).

        Note:
            The full path to the downloaded package can be accessed via
            the :attr:`~pkgpath` property.

        :Example:
            For example usage, please refer to this module's
            :mod:`docstring <ppklib.pip>`.

        """
        try:
            self._download()
            self._find()
        except Exception as err:
            ui.print_alert('\nThe following error occured, halting execution:\n', style='bold')
            print(*traceback.format_exception(err), sep='\n')
            self._cleanup()

    def _cleanup(self):
        """Class tear-down and internal cleanup method."""
        if isinstance(self._tmpdir, tempfile.TemporaryDirectory):
            self._tmpdir.cleanup()
        else:
            for f in glob(os.path.join(self._tmpdirname, '*')):
                os.unlink(f)
            os.removedirs(self._tmpdirname)

    def _download(self):
        """Using a subprocess call, download the package via pip.

        By design, the output from ``pip`` is streamed to the terminal
        and therefore not captured by a ``subprocess.PIPE``.

        The ``--only-binary=:all:`` argument is added to the pip command
        if *any* of the following arguments are passed, as this is a
        requirement by pip, unless ``--no_deps`` is specified.

            - ``--only_binary``
            - ``--platform``
            - ``--python_version``

        If the ``pip download`` fails for any reason (returning a
        non-zero exit code), the program is exited with an exit code of 1
        and a force cleanup is performed.

        """
        # pylint: disable=too-many-branches
        report_and_exit = False  # Escape if the pip error thrown is not expected.
        # Use the package name as passed into the CLI, as this *might* contain
        # a specific version to be downloaded.
        cmd = ['pip', 'download', '-d', self._tmpdirname]
        # Alter the pip command with user args from the CLI.
        if self._reqfile:
            # Download from requirements file.
            cmd.extend(['-r', self._reqfile])
        else:
            # Download from package name.
            pkg = f'{self._name}=={self._version}' if self._version else self._name
            cmd.extend([pkg])
        if not self._args.get('use_local'):
            cmd.extend(['-i', 'https://pypi.org/simple/'])
        if self._args.get('no_cache'):
            cmd.extend(['--no-cache'])
        if self._args.get('platform'):
            cmd.extend(['--platform', self._args['platform']])
        if self._args.get('python_version'):
            cmd.extend(['--python-version', self._args['python_version']])
        # Always add the ---only-binary=:all: arg if the platform or
        # py version are specified. This is a requirement by pip, unless
        # --no-deps is specified.
        if any((self._args.get('only_binary'),
                self._args.get('platform'),
                self._args.get('python_version'))):
            if self._args.get('no_deps'):
                cmd.extend(['--no-deps'])
            else:
                cmd.extend(['--only-binary', ':all:'])
        print('')  # Add blank line before pip output to aid readability.
        # No stdout pipe is used so pip's output streams to the terminal.
        with sp.Popen(cmd, stderr=sp.PIPE) as proc:
            _, stderr = proc.communicate()
            if proc.returncode:
                print('', stderr.decode(), sep='\n')
                if b'no matching distribution' in stderr.lower():
                    # Fix the missing (library not found) issue.
                    self._fix_missing(msg=stderr)
                else:  # nocover
                    report_and_exit = True
                if report_and_exit:  # nocover
                    ui.print_alert('\n[ERROR]: An error was thrown from pip. Exiting.\n')
                    self._cleanup()
                    sys.exit(1)
        print('')  # Add blank line after pip output to aid readability.

    def _find(self) -> None:
        """Find the downloaded target package and store the filename.

        For case agnostic searching, (e.g. in the case of libraries such
        as 'sqlalchemy' which downloads as 'SQLAlchemy'), the search is
        carried out using a :func:`filter` applied to the sorted return
        value from :func:`os.listdir`.

        If the target package is found in the download directory, the
        filename is stored to the :attr:`_pkg`: attribute.

        """
        if not self._reqfile:
            pkg = tuple(filter(lambda x: x.lower().startswith(self._name + '-'),
                               sorted(os.listdir(self._tmpdirname))))
            if pkg:
                self._pkg = pkg[0]
        else:
            self._pkg = self._tmpdirname

    def _fix_missing(self, msg: bytes):
        """Update the requirements file to fix the missing binary library.

        Args:
            msg (bytes): Error message thrown by pip to stderr, directly
                from the ``subprocess.Popen.communicate`` call.

        Using pip's error message, the offending package name is
        extracted. Then, a line (as shown below) is appended to the
        requirements file, instructing pip to download the source
        distribution::

            --no-binary=<pkg_name>

        Finally, re-call :meth:`_pip_download` to re-try the download
        with the modified requirements file.

        """
        pkg = self._parse_err__no_matching_dist(msg=msg)
        # Test if a requirements file is being used.
        if all((pkg, self._reqfile)):
            ui.print_(f'Modifying the requirements file and trying again for {pkg} ...',
                      fore='brightcyan')
            with open(self._reqfile, 'a', encoding='utf-8') as f:
                f.write(f'--no-binary={pkg}\n')
            self._download()

    @staticmethod
    def _parse_err__no_matching_dist(msg: bytes) -> str:
        """Extract the relevant package name from the error message.

        Args:
            msg (bytes): Error message directly from the
                Popen.communicate stderr pipe.

        Returns:
            str: Name of the offending package.

        """
        # pylint: disable=line-too-long
        pkg = None
        msg = msg.decode()
        rexp = re.compile(r'error: no matching distribution found for (?P<pkg>[\w-]+)(?:\\x1b)?', re.I)
        s = rexp.search(msg)
        if s:
            pkg = s.groupdict().get('pkg')
        return pkg

    def _set_tmpdir_name(self, name: str=None) -> None:
        """Set the name of the temp directory.

        Args:
            name (str, optional): Name of the temp directory from class
                instance. Defaults to None.

        If passed as None, a temp directory name is derived and used by
        pip, then destroyed afterwords. If a name is provided by the
        caller, this name is used instead.

        """
        # pylint: disable=consider-using-with  # No. Need to use the object throughout.
        if name is None:
            self._tmpdir = tempfile.TemporaryDirectory()
            self._tmpdirname = self._tmpdir.name
        else:
            self._tmpdirname = name
