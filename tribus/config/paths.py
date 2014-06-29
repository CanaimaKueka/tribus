#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

reprepro_dir = os.path.join(BASEDIR, 'test_repo')
sample_packages_dir = os.path.join(BASEDIR, 'package_samples')
selected_packages =  os.path.join(BASEDIR, 'tribus', 'config', 'data',
                                  'selected_packages.list')
distributions_path = os.path.join(BASEDIR, 'tribus', 'config', 'data',
                                  'dists-template')

