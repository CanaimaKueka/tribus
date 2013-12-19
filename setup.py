#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

Tribus setuptools script
========================

This script invokes the setup script for Tribus.

For more information about this file, see documentation on tribus/common/setup/utils.py

'''

from setuptools import setup

from tribus import BASEDIR
from tribus.common.setup.utils import get_setup_data

try:
    setup(**get_setup_data(BASEDIR))
except Exception, e:
    print e