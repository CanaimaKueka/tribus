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

tribus.tests.tribus_common_utils
================================

These are the tests for the tribus.common.utils module.

"""

from unittest import TestCase
from doctest import DocTestSuite
from tribus.common.setup import utils
from tribus.common.utils import cat_file


# class TestFileFunctions(TestCase):
#     def setUp(self):
#         self.string = 'Lola quiere comía'
#         self.test_file = '/tmp/test_cat_file'
#         with open(self.test_file, 'w') as f:
#         	f.write(self.string)
#         	f.close()
#     def test_cat_file(self):
#         self.assertEqual(cat_file(self.test_file), self.string)


def load_tests(loader, tests, ignore):
    tests.addTests(DocTestSuite(utils))
    return tests
