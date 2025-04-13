#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Purpose:   Library initialisation module.
"""

# Set path for relative imports.
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

# Bring commonly used classes to the surface.
from osv import OSVQuery
from pypi import PyPIQuery
