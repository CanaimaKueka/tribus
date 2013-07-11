#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s.sh [MÓDULO] [PARÁMETROS] [...]
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

from tribus.config.base import CONFDIR, DOCDIR
from tribus.common.utils import (get_path, cat_file, readconfig, get_requirements,
                                 get_dependency_links, get_classifiers, find_files,
                                 )

platforms = ('Any')
keywords = ('backup', 'archive', 'atom', 'rss', 'blog', 'weblog')
f_readme = get_path([DOCDIR, 'README'])
f_python_classifiers = get_path([CONFDIR, 'data', 'python-classifiers.list'])
f_python_dependencies = get_path([CONFDIR, 'data', 'python-dependencies.list'])
f_debian_dependencies = get_path([CONFDIR, 'data', 'debian-dependencies.list'])
f_exclude_sources = get_path([CONFDIR, 'data', 'exclude-sources.list'])
f_exclude_packages = get_path([CONFDIR, 'data', 'exclude-packages.list'])
f_exclude_patterns = get_path([CONFDIR, 'data', 'exclude-patterns.list'])
f_data_patterns = get_path([CONFDIR, 'data', 'include-data-patterns.list'])
f_workenv_preseed = get_path([CONFDIR, 'data', 'workenv-pkg-preseed.conf'])

exclude_sources = readconfig(filename=f_exclude_sources, conffile=False)
exclude_packages = readconfig(filename=f_exclude_packages, conffile=False)
exclude_patterns = readconfig(filename=f_exclude_patterns, conffile=False)
include_data_patterns = readconfig(filename=f_data_patterns, conffile=False)

long_description = cat_file(filename=f_readme)
classifiers = get_classifiers(filename=f_python_classifiers)
install_requires = get_requirements(filename=f_python_dependencies)
dependency_links = get_dependency_links(filename=f_python_dependencies)
debian_dependencies = readconfig(filename=f_debian_dependencies, conffile=False)
