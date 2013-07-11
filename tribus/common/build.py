#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.cmd import Command
from distutils.command.build import build as base_build
from docutils.core import Publisher
from docutils.writers import manpage
from sphinx.application import Sphinx
from cairosvg import svg2png

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.utils import get_path, find_files
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
                svg_code = open(svg_file, 'r').read()
            except Exception, e:
                print e

            try:
                png_file = open(os.path.splitext(svg_file)[0]+'.png', 'w')
            except Exception, e:
                print e

            try:
                svg2png(bytestring=svg_code, write_to=png_file)
            except Exception, e:
                print e

            png_file.close()
            log.debug("[%s.%s] %s > %s." % (__name__, self.__class__.__name__, svg_file,
                                            os.path.splitext(os.path.basename(svg_file))[0]+'.png'))


class build_html(Command):
    description = 'Compile .po files into .mo files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.debug("[%s.%s] Compiling documentation from RST sources." % (__name__,
                                                                         self.__class__.__name__))
        app = Sphinx(buildername='html', srcdir=get_path([DOCDIR, 'rst']),
                     confdir=get_path([DOCDIR, 'rst']), outdir=get_path([DOCDIR, 'html']),
                     doctreedir=get_path([DOCDIR, 'html', '.doctrees']))
        app.build(force_all=False, filenames=[])


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


class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('build_mo')
        self.run_command('build_img')
        self.run_command('build_html')
        self.run_command('build_man')
        base_build.run(self)
