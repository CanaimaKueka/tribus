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

"""

tribus.config.pkg
=================


"""

from tribus.config.base import CONFDIR, DOCDIR
from tribus.common.utils import get_path, cat_file, readconfig
from tribus.common.setup.utils import (get_requirements, get_dependency_links,
                                       get_classifiers)

platforms = ('Any')
keywords = ('Social Network',
            'Continuous Integration',
            'Source Code Management')
f_readme = get_path([DOCDIR, 'rst', 'readme.rst'])
f_python_classifiers = get_path([CONFDIR, 'data', 'python-classifiers.list'])
f_exclude_sources = get_path([CONFDIR, 'data', 'exclude-sources.list'])
f_exclude_packages = get_path([CONFDIR, 'data', 'exclude-packages.list'])
f_exclude_patterns = get_path([CONFDIR, 'data', 'exclude-patterns.list'])
f_include_data_patterns = get_path([CONFDIR, 'data',
                                    'include-data-patterns.list'])

f_python_dependencies = get_path([CONFDIR, 'data', 'python-dependencies.list'])
f_debian_run_dependencies = get_path([CONFDIR, 'data', 'debian-run-dependencies.list'])
f_debian_build_dependencies = get_path([CONFDIR, 'data', 'debian-build-dependencies.list'])

exclude_sources = readconfig(filename=f_exclude_sources, conffile=False)
exclude_packages = readconfig(filename=f_exclude_packages, conffile=False)
exclude_patterns = readconfig(filename=f_exclude_patterns, conffile=False)
include_data_patterns = readconfig(filename=f_include_data_patterns,
                                   conffile=False)

long_description = cat_file(filename=f_readme)
classifiers = get_classifiers(filename=f_python_classifiers)
install_requires = get_requirements(filename=f_python_dependencies)
dependency_links = get_dependency_links(filename=f_python_dependencies)

python_dependencies = readconfig(filename=f_python_dependencies,
                                 conffile=False, strip_comments=False)
debian_run_dependencies = readconfig(filename=f_debian_run_dependencies,
                                     conffile=False)
debian_build_dependencies = readconfig(filename=f_debian_build_dependencies,
                                       conffile=False)
