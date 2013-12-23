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

tribus.common.setup.report
=========================

This module contains common functions to process the information needed
by Setuptools/Distutils setup script.

'''

from distutils.cmd import Command


class report_setup_data(Command):
    description = 'Compress CSS files.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from pprint import pprint
        from tribus import BASEDIR
        from tribus.common.setup.utils import (get_packages, get_data_files,
                                               get_package_data,
                                               get_setup_data)
        from tribus.config.pkg import (exclude_sources, exclude_patterns,
                               include_data_patterns, exclude_packages)

        setup_data = get_setup_data(BASEDIR)
        packages = get_packages(path=BASEDIR,
                                exclude_packages=exclude_packages)
        data_files = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                                    exclude_files=exclude_sources + \
                                                  exclude_patterns)
        package_data = get_package_data(path=BASEDIR, packages=packages,
                                        data_files=data_files,
                                        exclude_files=exclude_sources + \
                                                      exclude_patterns,
                                        exclude_packages=exclude_packages)
        setup_data['data_files'] = data_files
        setup_data['package_data'] = package_data
        pprint(setup_data)
