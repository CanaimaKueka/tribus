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


# def get_i18n():

#     import locale
#     import gettext

#     from tribus.config.web import LOCALE_PATHS

#     lc, encoding = locale.getdefaultlocale()
#     gettext.install(True, localedir=None, unicode=1)
#     gettext.find('django', LOCALE_PATHS[0])
#     gettext.textdomain('django')
#     gettext.bind_textdomain_codeset('django', 'UTF-8')

#     return gettext.translation('django', LOCALE_PATHS[0], languages=lc, fallback=True).ugettext
