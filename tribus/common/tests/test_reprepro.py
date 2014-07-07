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

"""

These are the tests for the tribus.common.reprepro module.

"""

# import os
# from django.test import TestCase

# from tribus.common.utils import get_path
# from tribus.common.iosync import rmtree
# from tribus import BASEDIR

# SAMPLESDIR = get_path([BASEDIR, 'tribus', 'common', 'tests', 'samples'])


# class RepreproFunctions(TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_create_repository(self):
#         from tribus.common.reprepro import create_repository
#         test_repo = "/tmp/test_repo"
#         test_dist = os.path.join(SAMPLESDIR, 'distributions')
#         create_repository(test_repo, test_dist)
#         self.assertTrue(os.path.isdir(test_repo))
#         self.assertTrue(os.path.isdir(os.path.join(test_repo, 'db')))
#         self.assertTrue(os.path.isdir(os.path.join(test_repo, 'dists')))
#         self.assertTrue(os.path.isfile(os.path.join(test_repo, 'conf',
#                                                     'distributions')))
#         rmtree(test_repo)

#     def test_include_deb(self):
#         # Para probar esta funcion necesitaria acceso a internet y a un
#         # repositorio que no este caido
#         pass

#     def test_reset_repository(self):
#         # Tambien necesito llenar el repositorio previamente
#         pass
#         #from tribus.common.reprepro import  reset_repository
