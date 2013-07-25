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
import sys
import gtk
import gettext
import locale

from tribus.settings.gtk import LOCALEDIR
from tribus.common.utils import get_path
from tribus.gtk.main import Main
from tribus.gtk.constructor import UserMessage
from tribus.gtk.translator import MAIN_ROOT_ERROR_TITLE, MAIN_ROOT_ERROR_MSG

gtk.gdk.threads_init()

if __name__ == "__main__":
    settinglocale = locale.setlocale(locale.LC_ALL, '')
    naminglocale = get_path([
        LOCALEDIR, locale.getlocale()[0], 'LC_MESSAGES', '%s.mo' % localedomain
        ])

    try:
        gettext.GNUTranslations(open(naminglocale, 'rb')).install()
    except Exception:
        gettext.NullTranslations().install()

    if os.geteuid() != 0:
        dialog = UserMessage(
            message = MAIN_ROOT_ERROR_MSG, title = MAIN_ROOT_ERROR_TITLE,
            type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_OK,
            c_1 = gtk.RESPONSE_OK, f_1 = sys.exit, p_1 = (1,)
            )
    else:
        app = Main()
        gtk.main()
        sys.exit()
