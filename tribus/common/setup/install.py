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

tribus.common.setup.install
===========================


'''

from distutils.command.install_data import install_data as base_install_data
from distutils.command.build_py import build_py as base_build_py

from tribus.config.base import BASEDIR
from tribus.common.setup.utils import get_data_files, get_package_data
from tribus.common.logger import get_logger
from tribus.config.pkg import exclude_sources, exclude_patterns, include_data_patterns, exclude_packages

log = get_logger()

class build_py(base_build_py):
    def finalize_options(self):
        base_build_py.finalize_options(self)
    	data = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                              exclude_files=exclude_sources+exclude_patterns)
    	self.package_data = get_package_data(path=BASEDIR, packages=self.packages,
    										 data_files=data, exclude_files=exclude_sources+exclude_patterns,
		                                     exclude_packages=exclude_packages)
    	self.data_files = self.get_data_files()


class install_data(base_install_data):
    def finalize_options(self):
        base_install_data.finalize_options(self)
        self.data_files = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                                         exclude_files=exclude_sources+exclude_patterns)