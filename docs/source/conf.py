#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import sys
from datetime import datetime as dt

sys.path.insert(0, os.path.realpath('../../'))
from ppklib.libs._version import __version__


# -- Project information -----------------------------------------------------

project = 'ppklib'
copyright = f'2025 | s3dev | version {__version__}'
author = 'The Developers'
version = __version__
release = __version__


# -- General configuration ---------------------------------------------------

html_theme = 'sphinx_rtd_theme'
# Shorten doc'd method names to the name only, not the path.
add_module_names = False
autodoc_default_options = {
                           'exclude-members': ('__dict__, __module__, __weakref__'),
                           'inherited-members': False,
                           'members': True,
                           'member-order': 'bysource',
                           'private-members': True,
                           'show-inheritance': True,
                          }
#exclude_patterns = ['htg__*.rst', 'auth.rst']
extensions = ['sphinx.ext.autodoc', 
              'sphinx.ext.ifconfig', 
              'sphinx.ext.intersphinx',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon', 
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx_copybutton',
              'sphinx_git']
autodoc_mock_imports = [
                        'utils4',
                       ]
html_copy_source = False
html_css_files = ['css/s5defs-rules.css']
html_logo = '_static/img/s3dev_tri_white_sm.png'
html_static_path = ['_static']
html_search_language = 'en'
html_show_copyright = True
html_show_sourcelink = False
html_show_sphinx = False
html_title = f'{project} - v{__version__} Documentation'
master_doc = 'index'
mathjax_path = 'js/mathjax.js'
numfig = True
pygments_style = 'sphinx'
source_suffix = {'.rst': 'restructuredtext' }
templates_path = ['_templates']
todo_include_todos = True


# -- Epilog ------------------------------------------------------------------
# These items are included at the end of each source file.
# This is a useful place to keep file paths or variables which are used 
# throughout.

dtme = dt.now().strftime('%d %b %Y')
rst_epilog = f"""

.. |lastupdated| replace:: Last updated: {dtme}

.. include:: _static/css/s5defs.txt

"""

