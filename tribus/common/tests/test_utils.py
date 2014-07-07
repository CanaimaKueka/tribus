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

import os
from django.test import TestCase
from doctest import DocTestSuite

from tribus.common import utils


class TestIOFunctions(TestCase):

    def setUp(self):
        from tribus.common.utils import get_path
        from tribus.common.iosync import makedirs, touch, ln, rmtree

        self.tmpdir = get_path(['/', 'tmp', 'test_io'])
        self.tmpdir_1 = get_path([self.tmpdir, '1'])
        self.tmpdir_2 = get_path([self.tmpdir, '2'])
        self.tmpfile_1 = get_path([self.tmpdir_1, '1.txt'])
        self.tmpfile_2 = get_path([self.tmpdir_2, '2.txt'])
        self.tmpfile_3 = get_path([self.tmpdir_2, '3.log'])
        self.tmpfile_4 = get_path([self.tmpdir_2, '4.txt'])
        self.tmpfile_5 = get_path([self.tmpdir, '5.log'])
        self.tmpfile_6 = get_path([self.tmpdir, '6.py'])

        if os.path.isdir(self.tmpdir):
            rmtree(self.tmpdir)

        makedirs(self.tmpdir_1)
        makedirs(self.tmpdir_2)
        touch(self.tmpfile_1)
        touch(self.tmpfile_2)
        touch(self.tmpfile_3)
        touch(self.tmpfile_5)
        touch(self.tmpfile_6)
        ln(self.tmpfile_3, self.tmpfile_4)

    def tearDown(self):
        from tribus.common.iosync import rmtree
        if os.path.isdir(self.tmpdir):
            rmtree(self.tmpdir)

    def test_list_files(self):
        from tribus.common.utils import list_files
        self.assertEqual(sorted(list_files(path=self.tmpdir)),
                         sorted(['/tmp/test_io/5.log', '/tmp/test_io/6.py']))

    def test_list_files_is_file(self):
        from tribus.common.utils import list_files
        self.assertTrue(os.path.isfile(sorted(list_files(path=self.tmpdir))[1]))

    def test_find_files(self):
        from tribus.common.utils import find_files
        self.assertEqual(sorted(find_files(path=self.tmpdir, pattern='*.txt')),
                         sorted(['/tmp/test_io/1/1.txt',
                                 '/tmp/test_io/2/2.txt',
                                 '/tmp/test_io/2/4.txt']))

    def test_find_files_is_symlink(self):
        from tribus.common.utils import find_files
        self.assertTrue(os.path.islink(sorted(find_files(path=self.tmpdir,
                                                         pattern='*.txt'))[2]))

    def test_list_dirs(self):
        from tribus.common.utils import list_dirs
        self.assertEqual(sorted(list_dirs(path=self.tmpdir)),
                         sorted(['/tmp/test_io/1', '/tmp/test_io/2']))


def load_tests(loader, tests, ignore):
    tests.addTests(DocTestSuite(utils))
    return tests
