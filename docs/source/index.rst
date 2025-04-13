============================
ppklib Library Documentation
============================

.. contents:: Page Contents
    :local:
    :depth: 1


Overview
========
The ``ppklib`` library is a CPython project which provides the lower-level
core functionality to the primary `ppk`_ project. Generally, it is 
recommended to use ``ppk`` as opposed to interacting with this library 
directly; unless *specific* functionality is required.

As of ``ppk`` version 0.5.0, the core functionality has been moved out of 
``ppk`` into this library to enable other projects to take advantage of 
``ppk``'s vulnerability checking toolset. 

The following vulnerability tests are available:

 - **MD5 checksum:** The hash of the downloaded file is compared with the hash for the same file, 
   as stored by PyPI.

 - **Security vulnerabilities (Snyk):** The `Snyk security database <snyk_seccheck_>`_ can be 
   searched to determine if any vulnerabilities have been discovered and reported in the specific 
   library.

 - **Security vulnerabilities (PyPA):** The `PyPA  advisory database <pypa_seccheck_>`_ can be 
   searched (via the `PyPI JSON API <pypi_jsonapi_>`_) to determine if any 
   `vulnerabilities <pypi_knownvuln_>`_ have been discovered and reported in the specific library.

 - **Security vulnerabilities (OSV):** The `Open Source Vulnerabilities <osvweb_>`_ database can
   be searched (via the `OSV API <osvapi_>`_) to determine if any vulnerabilities have been 
   discovered and reported for a specific library.

 - **Code scanning:** Integration coming soon, via the `badsnakes`_ project.


Getting Started
===============

Downloading and installing
--------------------------
Likely, the easiest method for downloading and installing ``ppklib`` is 
through ``pip``, *after* activating the appropriate virtual environment, as::

    pip install ppklib


.. important:: 
    If using the `ppk` project, this library *must* be installed the same
    virtual environment which is used to run ``ppk``.

Basic usage
-----------
Basic example usage follows. For further detail and guidance please refer 
to the :ref:`using-the-library` section.

- Option 1) Download ``pandas`` (and dependencies) via ``pip``::

    from ppklib.pip import Download

    pipdl = Download('pandas')
    pipdl.get()

    # Display the path to the downloaded target package.
    pipdl.pkgpath

    # Optional cleanup after the wheels are no longer needed.
    pipdl.cleanup()


- Option 2) Download ``pandas`` version 2.2.3 for Windows and Python 3.13 
  into a specified download directory::

    from ppklib.pip import Download

    pipdl = Download('pandas',
                     version='2.2.3',
                     args={'platform': 'win_amd64', 'python_version': '313'},
                     tmpdir='/tmp/c0ff33')
    pipdl.get()

    # Display the path to the downloaded target package.
    pipdl.pkgpath

    # Optional cleanup after the wheels are no longer needed.
    pipdl.cleanup()


.. _using-the-library:

Using the Library
=================
This documentation suite contains detailed explanation and example usage 
for each of the library's importable modules. For detailed documentation, 
usage examples and links the source code itself, please refer to the 
:ref:`library-api` page.

If there is a specific module or method which you cannot find, a 
**search** field is built into the navigation bar to the left.


.. _troubleshooting:

Troubleshooting
===============
No guidance at this time.

Questions or Issues
-------------------
If you have any issues or questions with your installation, please refer
to the :ref:`troubleshooting` section, or feel free to 
:ref:`contact us <contact-us>`.


Documentation Contents
======================
.. toctree::
    :maxdepth: 1

    library
    libs_changelog
    contact


Indices and Tables
==================
* :ref:`genindex`
* :ref:`modindex`


.. rubric:: Footnotes

.. _PyPI: https://pypi.org/project/utils4/#files
.. _GitHub: https://github.com/s3dev/utils4/
.. _GitHub Releases: https://github.com/s3dev/utils4/releases

.. _badsnakes: https://pypi.org/project/badsnakes/
.. _docs: https://ppklib.readthedocs.io/en/latest/
.. _osvapi: https://google.github.io/osv.dev/api/
.. _osvweb: https://osv.dev/
.. _ppk: https://github.com/s3dev/ppk/
.. _pypa_seccheck: https://github.com/pypa/advisory-database
.. _pypi_jsonapi: https://docs.pypi.org/api/json/
.. _pypi_knownvuln: https://docs.pypi.org/api/json/#known-vulnerabilities
.. _snyk_seccheck: https://security.snyk.io/


|lastupdated|

