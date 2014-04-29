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

from django.test.testcases import TestCase
from tribus.web.cloud.models import Maintainer, Package, Details,\
Relation

'''

tribus.tests.tribus_web_cloud_models
================================

These are the tests for the tribus.web.cloud models.

'''

class RegistrationModelTests(TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass