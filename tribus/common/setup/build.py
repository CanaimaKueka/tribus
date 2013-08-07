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

tribus.common.setup.install
===========================


'''

import os
import sys
import shutil
from distutils.cmd import Command
from distutils.command.build import build as base_build
from docutils.core import Publisher
from docutils.writers import manpage
from sphinx.application import Sphinx
from sphinx.setup_command import BuildDoc as base_build_sphinx
from babel.messages.frontend import compile_catalog as base_compile_catalog

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.images import svg2png
from tribus.common.utils import get_path, find_files, list_dirs, list_files
from tribus.common.logger import get_logger

log = get_logger()


class build_img(Command):
    description = 'Compile SVG files into PNG images.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.debug("[%s.%s] Compiling PNG images from SVG sources." % (__name__,
                                                                      self.__class__.__name__))
        for svg_file in find_files(path=BASEDIR, pattern='*.svg'):
            try:
                svg2png(input_file=svg_file, output_file=os.path.splitext(svg_file)[0]+'.png')
            except Exception, e:
                print e

            log.debug("[%s.%s] %s > %s." % (__name__, self.__class__.__name__, svg_file,
                                            os.path.splitext(os.path.basename(svg_file))[0]+'.png'))


class build_man(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.debug("[%s.%s] Compiling manual from RST sources." % (__name__,
                                                                  self.__class__.__name__))
        pub = Publisher(writer=manpage.Writer())
        pub.set_components(reader_name='standalone', parser_name='restructuredtext',
                           writer_name='pseudoxml')
        pub.publish(argv=[u'%s' % get_path([DOCDIR, 'man', 'tribus.rst']),
                          u'%s' % get_path([DOCDIR, 'man', 'tribus.1'])])


class build_sphinx(base_build_sphinx):

    def get_sphinx_locale_list(self):
        return set(filter(None, list_dirs(get_path([DOCDIR, 'rst', 'i18n'])))) - set(['pot'])

    def run(self):
        for locale in self.get_sphinx_locale_list():
            base_build_sphinx.run(self)


class compile_catalog(base_compile_catalog):

    def get_sphinx_pot_list(self):
        return filter(None, list_files(get_path([DOCDIR, 'rst', 'i18n', 'pot'])))

    def run(self):
        base_compile_catalog.run(self)

        for potfile in self.get_sphinx_pot_list():
            base_compile_catalog.initialize_options(self)
            self.domain = os.path.splitext(os.path.basename(potfile))[0]
            self.directory = get_path([DOCDIR, 'rst', 'i18n']).replace(BASEDIR+os.sep, '')
            self.use_fuzzy = True
            base_compile_catalog.run(self)


class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('update_catalog')
        self.run_command('compile_catalog')
        self.run_command('build_img')
        self.run_command('build_sphinx')
        self.run_command('build_man')
        base_build.run(self)
