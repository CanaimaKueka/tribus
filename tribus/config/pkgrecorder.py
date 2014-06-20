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

import os
from tribus.config.base import BASEDIR

LOCAL_ROOT = os.path.join('file://', BASEDIR, 'test_repo')
CANAIMA_ROOT = 'http://paquetes.canaima.softwarelibre.gob.ve'
SAMPLES_DIR = os.path.join(BASEDIR, 'package_samples')

PACKAGE_FIELDS = {'Package': 'Name', 'Description': 'Description',
                  'Homepage': 'Homepage', 'Section': 'Section',
                  'Priority': 'Priority', 'Essential': 'Essential',
                  'Bugs': 'Bugs', 'Multi-Arch': 'MultiArch'}

DETAIL_FIELDS = {'Version': 'Version', 'Architecture': 'Architecture',
                 'Size': 'Size', 'MD5sum': 'MD5sum', 'Filename': 'Filename',
                 'Installed-Size': 'InstalledSize'}

relation_types = ['pre-depends', 'depends', 'recommends', 'suggests',
                  'provides', 'enhances', 'breaks', 'replaces', 'conflicts']

codenames = {'aponwao': '2.1', 'roraima': '3.0', 'auyantepui': '3.1',
             'kerepakupai': '4.0', 'kukenan': '4.1'}
