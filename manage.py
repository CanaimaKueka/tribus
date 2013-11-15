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

'''

Django management script for Tribus
===================================

This file is an entry point for managing Tribus in development mode.

'''


if __name__ == "__main__":

    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
