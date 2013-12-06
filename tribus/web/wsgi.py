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

import sys
import os
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'tribus.config.web'

base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'virtualenv'))
os.environ['PATH'] = os.path.join(base, 'bin') + os.pathsep + os.environ['PATH']
site.addsitedir(os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages'))
sys.prefix = base
sys.path.insert(0, base)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
