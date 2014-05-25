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

from tribus.config.brand import *
from tribus.config.web import DEBUG


def default_context(request):
    return {
        'render_css': ['normalize', 'bootstrap', 'fonts', 'font-awesome',
                       'tribus', 'tribus-responsive'],
        'render_js': ['angular', 'angular.bootstrap', 'angular.bootstrap',
                      'angular.resource', 'elements.angular',
                      'controllers.angular', 'services.angular',
                      'search.angular'],
        'tribus_distro': TRIBUS_DISTRO,
        'tribus_role_1': TRIBUS_ROLE_1,
        'tribus_role_2': TRIBUS_ROLE_2,
        'tribus_role_3': TRIBUS_ROLE_3,
        'DEBUG': DEBUG,
    }

