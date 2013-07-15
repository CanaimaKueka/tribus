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

from tribus import BASEDIR

NAME = u'Tribus'
VERSION = (0, 1, 0, 'alpha', 0)
URL = u'http://git.canaima.softwarelibre.gob.ve/?p=tribus.git;a=summary'
AUTHOR = u'Desarrolladores de Tribus'
AUTHOR_EMAIL = u'desarrolladores@canaima.softwarelibre.gob.ve'
DESCRIPTION = (u'Red social para la gestión de comunidades de Software Libre.'),
LICENSE = u'GPL'


if BASEDIR == '/usr/share/pyshared':
    CONFDIR = '/etc/tribus'
    BINDIR = '/usr/bin'
    SHAREDIR = '/usr/share/tribus'
    DOCDIR = '/usr/share/doc/tribus'
    ICONDIR = '/usr/share/icons/hicolor'
    LOCALEDIR = '/usr/share/locale'
else:
    CONFDIR = BASEDIR+'/tribus/config'
    BINDIR = BASEDIR
    SHAREDIR = BASEDIR
    DOCDIR = BASEDIR+'/tribus/data/docs'
    LOCALEDIR = BASEDIR+'/tribus/i18n'
    ICONDIR = BASEDIR+'/tribus/data/icons'

# forbidden_filename_chars = {
#     '/':'', ':':'', 'http':'', 'file':'', 'ftp':'', '?':'', '=':'', '&':'',
#     '-':'', '(':'', ')':'', '+':'', '-':'', '#':'', '$':'', '%':'', '@':'',
#     '|':'', '~':'', '_':'', ',':'', ';':'', '!':''
#     }

# bs = 16*1024
# BAR_ICON = ICONDIR+'/48x48/apps/c-s-gui.png'
# BUILD_ICON = GUIDIR+'/images/build-image.png'
# PROFILE_ICON = GUIDIR+'/images/create-profile.png'
# TEST_ICON = GUIDIR+'/images/test-image.png'
# SAVE_ICON = GUIDIR+'/images/save-image.png'
# BANNER_IMAGE = GUIDIR+'/images/banner.png'
# ABOUT_IMAGE = GUIDIR+'/images/logo.png'
# VERSION_FILE = SHAREDIR+'/VERSION'
# AUTHORS_FILE = SHAREDIR+'/AUTHORS'
# LICENSE_FILE = SHAREDIR+'/LICENSE'
# TRANSLATORS_FILE = SHAREDIR+'/TRANSLATORS'

# window_height = 550
# window_width = 700
# spacing = 0
# padding = 0
# borderwidth = 5
# expand = False
# fill = False
# homogeneous = False

# app_name = 'Canaima Semilla'
# app_version = '@APPVERSION@'
# app_copyright = 'Copyright (C) 2010 - 2012, Luis Alejandro Martínez Faneyth'
# app_url = 'http://code.google.com/p/canaima-semilla'
# app_description = 'Generador de distribuciones derivadas'
# default_profile_email = 'desarrolladores@canaima.softwarelibre.gob.ve'
# default_profile_name = 'sabor'
# default_profile_author = 'Equipo de Desarrollo del Proyecto Canaima'
# default_profile_url = 'http://canaima.softwarelibre.gob.ve/'
# canaima_repo = 'http://paquetes.canaima.softwarelibre.gob.ve/'
# debian_repo = 'http://ftp.us.debian.org/debian/'
# ubuntu_repo = 'http://archive.ubuntu.com/ubuntu/'
# section_default = 'main'
# google = 'http://74.125.113.99'
# supported_locales = '/usr/share/i18n/SUPPORTED'
# apt_templates = '/usr/share/python-apt/templates'
# tempdir = '/tmp/canaima-semilla/'

# supported_arch = ['i386', 'amd64']
# supported_media = ['iso', 'usb', 'iso-hybrid']
# cs_distros = ['debian', 'ubuntu', 'canaima']
# debian_sections = ['main', 'contrib', 'non-free']
# ubuntu_sections = ['main', 'universe', 'multiverse', 'restricted']
# canaima_sections = ['main', 'aportes', 'no-libres']
