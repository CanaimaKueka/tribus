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

import os

from canaimasemilla.common import ConfigMapper

curdir = os.path.abspath(os.getcwd())

if curdir == '/usr/bin':
    GUIDIR = '/usr/share/pyshared/canaimasemilla'
    CONFDIR = '/etc/canaima-semilla/gui'
    BINDIR = '/usr/bin'
    CSBIN = 'c-s'
    SHAREDIR = '/usr/share/canaima-semilla'
    COREDIR = SHAREDIR+'/scripts'
    PROFILEDIR = SHAREDIR+'/profiles'
    DOCDIR = '/usr/share/doc/canaima-semilla/html'
    ICONDIR = '/usr/share/icons/hicolor'
    LOCALEDIR = '/usr/share/locale'
else:
    SRCDIR = curdir
    GUIDIR = SRCDIR+'/canaimasemilla'
    CONFDIR = SRCDIR+'/config/gui'
    BINDIR = SRCDIR
    CSBIN = 'c-s-core.sh'
    SHAREDIR = SRCDIR
    COREDIR = SRCDIR+'/scripts'
    PROFILEDIR = SRCDIR+'/profiles'
    DOCDIR = SRCDIR+'/documentation/html'
    ICONDIR = SRCDIR+'/icons/hicolor'
    LOCALEDIR = SRCDIR+'/locale'

forbidden_filename_chars = {
    '/':'', ':':'', 'http':'', 'file':'', 'ftp':'', '?':'', '=':'', '&':'',
    '-':'', '(':'', ')':'', '+':'', '-':'', '#':'', '$':'', '%':'', '@':'',
    '|':'', '~':'', '_':'', ',':'', ';':'', '!':''
    }
bs = 16*1024
BAR_ICON = ICONDIR+'/48x48/apps/c-s-gui.png'
BUILD_ICON = GUIDIR+'/images/build-image.png'
PROFILE_ICON = GUIDIR+'/images/create-profile.png'
TEST_ICON = GUIDIR+'/images/test-image.png'
SAVE_ICON = GUIDIR+'/images/save-image.png'
BANNER_IMAGE = GUIDIR+'/images/banner.png'
ABOUT_IMAGE = GUIDIR+'/images/logo.png'
VERSION_FILE = SHAREDIR+'/VERSION'
AUTHORS_FILE = SHAREDIR+'/AUTHORS'
LICENSE_FILE = SHAREDIR+'/LICENSE'
TRANSLATORS_FILE = SHAREDIR+'/TRANSLATORS'

configload = ConfigMapper(CONFDIR)

for configoption, configvalue in configload.iteritems():
    exec str(configoption)+' = '+str(configvalue)
