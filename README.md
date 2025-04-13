# ppklib - Python Package Check Library

[![PyPI - Version](https://img.shields.io/pypi/v/ppklib?style=flat-square)](https://pypi.org/project/ppklib)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/ppklib?style=flat-square)](https://pypi.org/project/ppklib)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ppklib?style=flat-square)](https://pypi.org/project/ppklib)
[![PyPI - Status](https://img.shields.io/pypi/status/ppklib?style=flat-square)](https://pypi.org/project/ppklib)
[![Static Badge](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](https://pypi.org/project/ppklib)
[![Static Badge](https://img.shields.io/badge/code_coverage-100%25-brightgreen?style=flat-square)](https://pypi.org/project/ppklib)
[![Static Badge](https://img.shields.io/badge/pylint_analysis-100%25-brightgreen?style=flat-square)](https://pypi.org/project/ppklib)
[![Documentation Status](https://readthedocs.org/projects/ppklib/badge/?version=latest&style=flat-square)](https://ppklib.readthedocs.io/en/latest/)
[![PyPI - License](https://img.shields.io/pypi/l/ppklib?style=flat-square)](https://opensource.org/license/gpl-3-0)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/ppklib?style=flat-square)](https://pypi.org/project/ppklib)

The core functionality library behind the [ppk](https://github.com/s3dev/ppk) project.


## Overview
This library provides the lower-level core functionality to the primary [`ppk`](https://github.com/s3dev/ppk) project.

As of `ppk` version 0.5.0, the core functionality has been moved out of `ppk` into this library to enable other projects to take advantage of `ppk`'s vulnerability checking toolset. 

The following vulnerability tests are available:
 - **MD5 checksum:** The hash of the downloaded file is compared with the hash for the same file, as stored by PyPI.
 - **Security vulnerabilities (Snyk):** The [Snyk security database](https://security.snyk.io/) can be searched to determine if any vulnerabilities have been discovered and reported in the specific library.
 - **Security vulnerabilities (PyPA):** The [PyPA  advisory database](https://github.com/pypa/advisory-database) can be searched (via the [PyPI JSON API](https://docs.pypi.org/api/json/)) to determine if any [vulnerabilities](https://docs.pypi.org/api/json/#known-vulnerabilities) have been discovered and reported for a specific library.
 - **Security vulnerabilities (OSV):** The [Open Source Vulnerabilities](https://osv.dev/) database can be searched (via the [OSV API](https://google.github.io/osv.dev/api/)) to determine if any vulnerabilities have been discovered and reported for a specific library.
 - **Code scanning:** Integration coming soon, via the [`badsnakes`](https://pypi.org/project/badsnakes/) project.


## Getting Started

### Downloading and installing
Likely, the easiest method for downloading and installing `ppklib` is through `pip`, *after* activating the appropriate virtual environment, as:
```
pip install ppklib
```

> **Note:**
> If using the `ppk` project, this library *must* be installed into the same virtual environment which is used to run `ppk`.

### Basic usage
Basic example usage follows. For further detail and guidance please refer to the [project's documentation](https://ppklib.readthedocs.io/en/latest/).

**Download `pandas` (and dependencies) via `pip`:**
```python
from ppklib.pip import Download

pipdl = Download('pandas')
pipdl.get()

# Display the path to the downloaded target package.
pipdl.pkgpath

# Optional cleanup after the wheels are no longer needed.
pipdl.cleanup()
```

**Download `pandas` version 2.2.3 for Windows and Python 3.13 into a specified download directory:**

```python
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
```

