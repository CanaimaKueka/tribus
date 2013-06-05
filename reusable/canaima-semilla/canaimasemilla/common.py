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

import os, ConfigParser

def listdirfullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def ConfigMapper(confdir):
    dictionary = {}
    config = ConfigParser.ConfigParser()
    conffiles = listdirfullpath(confdir)
    configuration = config.read(conffiles)
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        for option in options:
            try:
                giveme = config.get(section, option)
                if section == 'array':
                    process = giveme[1:-1].split(',')
                elif section == 'boolean':
                    process = giveme
                elif section == 'integer':
                    process = int(giveme)
                else:
                    process = '"'+giveme+'"'
                dictionary[option] = process
            except:
                dictionary[option] = None
    return dictionary
