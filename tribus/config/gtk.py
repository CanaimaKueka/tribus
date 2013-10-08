# #!/usr/bin/env python
# # -*- coding: utf-8 -*-


# import os

# curdir = os.path.abspath(os.getcwd())

# if curdir == '/usr/bin':
#     GUIDIR = '/usr/share/pyshared/canaimasemilla'
#     CONFDIR = '/etc/canaima-semilla/gui'
#     BINDIR = '/usr/bin'
#     CSBIN = 'c-s'
#     SHAREDIR = '/usr/share/canaima-semilla'
#     COREDIR = SHAREDIR+'/scripts'
#     PROFILEDIR = SHAREDIR+'/profiles'
#     DOCDIR = '/usr/share/doc/canaima-semilla/html'
#     ICONDIR = '/usr/share/icons/hicolor'
#     LOCALEDIR = '/usr/share/locale'
# else:
#     SRCDIR = curdir
#     GUIDIR = SRCDIR+'/canaimasemilla'
#     CONFDIR = SRCDIR+'/config/gui'
#     BINDIR = SRCDIR
#     CSBIN = 'c-s-core.sh'
#     SHAREDIR = SRCDIR
#     COREDIR = SRCDIR+'/scripts'
#     PROFILEDIR = SRCDIR+'/profiles'
#     DOCDIR = SRCDIR+'/documentation/html'
#     ICONDIR = SRCDIR+'/icons/hicolor'
#     LOCALEDIR = SRCDIR+'/locale'

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
