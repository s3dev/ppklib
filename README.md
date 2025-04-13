# ppk - Python Package Check

A Python library download and vulnerability-checking tool used to help safely transfer libraries to secured environments.


## Overview
If you maintain an offline, or air-gapped pip repository in a secured environment, it's important to keep that repo clean and free from libraries with known vulnerabilities, or malicious code. This is where `ppk` comes in.

The `ppk` application comes in two parts, the *packer* and the *unpacker*. The packer is installed on an internet connected PC and used to retrieve libraries (and their dependencies) from [PyPI](https://pypi.org/), via `pip`. If the downloaded files pass security checks, they are packed into an encrypted and password protected archive. This archive is transferred to the secured environment and unpacked into the local pip repo by `ppk`'s unpacker.


## How does it work?
The `ppk` packer utility is, at its very core, a wrapper around the `pip download` command - with added security checking functionality.

Using the supplied arguments, a Python library (and its dependencies) are downloaded from [PyPI](https://pypi.org/) using a subprocess call to `pip download`. Once the download has completed, a series of vulnerability checks are conducted on *each* downloaded file to help ensure the code contained within is not reported to have vulnerabilities or to be malicious.

The following vulnerability tests are conducted on *each* downloaded file:
 - **MD5 checksum:** The hash of the downloaded file is compared with the hash for the same file, as stored by PyPI.
 - **Security vulnerabilities:** The [Snyk security database](https://security.snyk.io/) is searched to determine if any vulnerabilities have been discovered and reported in the specific library.
 - **Code scanning:** Coming soon, via the [`badsnakes`](https://pypi.org/project/badsnakes/) project which is currently under development.

If all security checks pass, an encrypted `.7z` archive is created on your desktop containing the downloaded libraries. This archive is then transferred to the secured environment. 

Finally, `ppk`'s *unpacker* utility is used to unpack this archive into the environment's secured local pip repository; where a user can install the library using a standard `pip install <package-name>` command from the terminal.


## Getting started
This section provides a quick-start guide to getting up and running. The `ppk` utility is generally installed to the `/usr/local/bin` directory, and can be accessed at any time by simply typing `ppk` into the terminal.

For example, the help menu can be displayed at any point by providing the `--help` argument:

``` bash
$ ppk --help
``` 

### Downloading and installing
The simple steps below guide you through downloading, building and installing `ppk`. 

**Reminder:** `ppk` must be installed on the secured environment *and* on an internet-connected PC.

> **Important Note:** 
> `ppk` is designed to run on Linux systems.
>
>However, as the *packer* is written in CPython, it can be adapted to Windows (with minimal effort) and does *not* require installation; it can be run directly from the source download.
>
> If requiring an *unpacker* for Windows, please see the *Unpacking on Windows* section at the end of this README.

1. Create a Python virtual environment, from which `ppk` will be run.
1. Activate the newly created virtual environment.
1. Download the source from [GitHub](https://github.com/s3dev/ppk/archive/refs/heads/master.zip).
1. Unpack the downloaded zip file, and navigate into the extracted directory.
1. Run the `build.sh` script to compile the unpacker for your CPU and create the source distribution for install.
1. Copy the `dist/ppk-<version>.tar.gz` archive to your `~/Downloads` directory, and unpack.
1. Navigate to your `~/Downloads/ppk-<version>` directory and run `install.sh`.
	- Enter the path to the virtual environment created above. For example: `/var/venvs/ppk311`
	- Enter the installation path for `ppk`. The default is `/usr/local/bin`.
1. Test the installation was successful by typing: `ppk --help`.
1. [Optional]: Update the *path to the local pip repo* in the `lib/upack.d/bin/config.toml` file, updating the `dir_pip_repo` key. This is the path into which the unpacker will transfer the libraries. 
1. [Optional]: Update the name of the program used to refresh the pip repo in the `lib/config.json` file, updating the `pip_refresh_prog` key. This program is called by `ppk` after each unpacking.


## Using `ppk` to download from PyPI
The following headings demonstrate various methods - in increasing complexity - by which `ppk` can be used to download a Python library and dependencies from PyPI.

**Note:** All of the following examples must be run on an PC *with internet access*.

#### Simplest
The following example demonstrates a simplified use of the utility to download the latest version of the  `pandas` library:

``` bash
# Download pandas
$ ppk pandas 
```

#### Specifying the library version
The following example demonstrates how a *specific version* of the `pandas` library can be downloaded:

``` bash
# Download pandas version 2.0.1
$ ppk "pandas==2.0.1"
```

If the library version is not specified, the download will default to the latest version available.

#### Specifying the Python version
The following example demonstrates how a specific version of the `pandas` library can be downloaded, for a *specific version of Python*; in this case Python 3.11:

``` bash
# Download pandas version 2.0.1 for Python 3.11
$ ppk "pandas==2.0.1" --python_version=311
```

If the Python version is not specified, the download will default to the Python version of the current interpreter, or virtual environment.

#### Specifying the platform
There are times when a platform (or system architecture) will need to be supplied. For example, you are working on an amd64 architecture, but need a library compiled for a Linux aarch64 architecture - however the aarch64 PC is not connected to the internet.

The following example demonstrates how a specific version of the `pandas` library can be downloaded, for a specific version of Python; in this case Python 3.11 - and compiled for an aarch64 architecture:

``` bash
# Download pandas version 2.0.1 for Python 3.11, and an aarch64 CPU architecture
$ ppk "pandas==2.0.1" --python_version=311 --platform=manylinux2014_aarch64
```

If the platform is not specified, the download will default to the platform of the current interpreter.

#### Using a `requirements.txt` file
When needing to download several Python libraries (and their dependencies) at once, a `requirements.txt` file can be used. Within this file are specified the target libraries (and their version) to be downloaded.

For example, a sample file may look like:

```bash
numpy==1.26.1
pandas==2.0.1
python-dateutil==2.8.2
pytz==2023.3.post1
six==1.16.0
tzdata==2023.3
``` 

The following example demonstrates how to pass a `requirements.txt` file to `ppk`:

``` bash
# Download all libraries (and dependencies) in the specified file
$ ppk /path/to/requirements.txt
```


## Transferring and unpacking an encrypted archive
Once the Python libraries have been downloaded and tested, they are archived into an encrypted `.7z` file on your local desktop, ready for transfer to the secured environment. However, if the security checks fail, an archive is *not* created. For libraries which pass the security checks,  `ppk` is then used to *unpack* the encrypted archive containing the downloaded libraries onto the environment's secured local pip repository.

### 7zip 
Beginning with `ppk` version 0.2.0, we introduced *encrypted, password-protected archiving* to help make the archive transfer more secure, and requires 7zip to be installed on your system.

If you don't have 7zip available, it is [freely available](https://7-zip.org/faq.html) under the [GNU LGPL licence](https://7-zip.org/faq.html#developer_faq).

-  **Linux:** [p7zip for Debian](https://packages.debian.org/sid/p7zip-full) can be installed with: `sudo apt install p7zip-full`
- **Windows:** [Download the EXE here](https://7-zip.org/)

### Verify and unpack an archive
First, transfer the encrypted archive (the `.7z` file) to the secured environment. Note: This environment must also have `ppk` installed. Refer to the installation guidance above if needed.

Next, use `ppk`'s unpacker to decrypt the archive and transfer the libraries into the local pip repo. For example, to decrypt and transfer the archive we downloaded earlier for `pandas` 2.0.1:

``` bash
$ ppk ~/Desktop/pandas-2.0.1-cp311-cp311-manylinux2014_x86_64.7z
```

When `ppk` detects a file extension of `.7z`, the unpacker utility is automatically called.

### Unpacking on Windows
The builtin unpacker utility is compiled for and designed to work on Unix/Linux systems only. If your pip repository is on a Windows system, a different unpacking approach will be required as you'll need the `upackw` executable, which can be downloaded from the [GitHub releases page](https://github.com/s3dev/upackw/releases). 

The basic steps are: 
1. Download the `upackw.exe` executable from GitHub.
1.  Unpack your `.7z` archive as:
 ``` cmd
> upackw.exe c:\path\to\archive\pandas-2.0.1-cp311-cp311-win_amd64.7z
 ```
Further detail and guidance can be found on the [project's GitHub page](https://github.com/s3dev/upackw).

