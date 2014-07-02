#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_path

NAME = 'Tribus'
VERSION = (0, 1, 0, 'alpha', 1)
URL = 'http://github.com/tribusdev/tribus'
AUTHOR = 'Tribus Developers'
AUTHOR_EMAIL = 'tribusdev@googlegroups.com'
DESCRIPTION = ('A Social Network to manage Free & '
               'Open Source Software communities.')
LICENSE = 'GPL3'


BINDIR = BASEDIR
SHAREDIR = BASEDIR
CONFDIR = get_path([BASEDIR, 'tribus', 'config'])
DATADIR = get_path([BASEDIR, 'tribus', 'data'])
DOCDIR = get_path([DATADIR, 'docs'])
LOCALEDIR = get_path([DATADIR, 'i18n'])
ICONDIR = get_path([DATADIR, 'icons'])
CHARMSDIR = get_path([DATADIR, 'charms'])
STATICDIR = get_path([DATADIR, 'static'])

PACKAGECACHE = BASEDIR + '/packagecache'  # XXX
