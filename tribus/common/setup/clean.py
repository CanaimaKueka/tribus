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

"""

import os
import shutil
from distutils.cmd import Command
from distutils.command.clean import clean as base_clean

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.utils import get_path, find_files, find_dirs
from tribus.common.logger import get_logger

log = get_logger()


class clean_img(Command):
    description = 'Remove compiled PNG files from source.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for png_file in find_files(path=BASEDIR, pattern='*.png'):
            if os.path.isfile(png_file):
                try:
                    os.unlink(png_file)
                    log.debug("[%s.%s] Removing \"%s\"." % (__name__,
                                                            self.__class__.__name__,
                                                            png_file))
                except Exception as e:
                    print e


class clean_pyc(Command):
    description = 'Remove compiled PNG files from source.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for pyc_file in find_files(path=BASEDIR, pattern='*.pyc'):
            if os.path.isfile(pyc_file):
                try:
                    os.unlink(pyc_file)
                    log.debug("[%s.%s] Removing \"%s\"." % (__name__,
                                                            self.__class__.__name__,
                                                            pyc_file))
                except Exception as e:
                    print e


class clean_css(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        CSSMIN_DIR = get_path(
            [BASEDIR,
             'tribus',
             'data',
             'static',
             'css',
             'min'])

        if os.path.isdir(CSSMIN_DIR):
            try:
                shutil.rmtree(CSSMIN_DIR)
                log.debug(
                    "[%s.%s] Removing \"%s\"." %
                    (__name__, self.__class__.__name__, CSSMIN_DIR))
            except Exception as e:
                print e


class clean_js(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        JSMIN_DIR = get_path(
            [BASEDIR,
             'tribus',
             'data',
             'static',
             'js',
             'min'])

        if os.path.isdir(JSMIN_DIR):
            try:
                shutil.rmtree(JSMIN_DIR)
                log.debug(
                    "[%s.%s] Removing \"%s\"." %
                    (__name__, self.__class__.__name__, JSMIN_DIR))
            except Exception as e:
                print e


class clean_sphinx(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for sphnxdir in [get_path([DOCDIR, 'html']),
                         get_path([DOCDIR, 'doctrees'])]:
            if os.path.isdir(sphnxdir):
                try:
                    shutil.rmtree(sphnxdir)
                    log.debug("[%s.%s] Removing \"%s\"." %
                              (__name__, self.__class__.__name__, sphnxdir))
                except Exception as e:
                    print e


class clean_man(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        man_file = get_path([DOCDIR, 'man', 'tribus.1'])
        if os.path.isfile(man_file):
            try:
                os.unlink(man_file)
                log.debug(
                    "[%s.%s] Removing \"%s\"." %
                    (__name__, self.__class__.__name__, man_file))
            except Exception as e:
                print e


class clean_mo(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for mo_file in find_files(path=BASEDIR, pattern='*.mo'):
            if os.path.isfile(mo_file):
                try:
                    os.unlink(mo_file)
                    log.debug(
                        "[%s.%s] Removing \"%s\"." %
                        (__name__, self.__class__.__name__, mo_file))
                except Exception as e:
                    print e


class clean_dist(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for dist_dir in ['dist', 'build', 'Tribus.egg-info']:
            dist_subdir = get_path([BASEDIR, dist_dir])
            if os.path.isdir(dist_subdir):
                try:
                    shutil.rmtree(dist_subdir)
                    log.debug("[%s.%s] Removing \"%s\"." %
                              (__name__, self.__class__.__name__,
                               dist_subdir))
                except Exception as e:
                    print e


class clean(base_clean):

    def run(self):
        self.run_command('clean_dist')
        self.run_command('clean_mo')
        self.run_command('clean_img')
        self.run_command('clean_js')
        self.run_command('clean_css')
        self.run_command('clean_sphinx')
        self.run_command('clean_man')
        self.run_command('clean_pyc')
        base_clean.run(self)
