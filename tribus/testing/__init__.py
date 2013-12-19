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

tribus.testing
==============

This file contains the entry point to the tribus tests.

'''

import sys
from django.test.utils import get_runner
from django.conf import settings


def runtests():
    runner = get_runner(settings)
    instance = runner(verbosity=1, interactive=False, failfast=True)
    failures = instance.run_tests(['testing'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()