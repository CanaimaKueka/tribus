#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.cmd import Command
from distutils.command.build import build as base_build
from docutils.core import Publisher
from docutils.writers import manpage
from cairosvg import svg2png

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.setup.utils import get_packages, get_package_data, get_data_files
from tribus.common.utils import get_path, find_files
from tribus.common.logger import get_logger
from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                               exclude_packages, exclude_sources, exclude_patterns,
                               include_data_patterns, platforms, keywords)
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
                png_code = svg2png(url=svg_file)
            except Exception, e:
                png_code = ''
                print e
    
            png_file = open(os.path.splitext(svg_file)[0]+'.png', 'w')
            png_file.write(png_code)
            png_file.close()
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


class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('compile_catalog')
        self.run_command('build_img')
        self.run_command('build_sphinx')
        self.run_command('build_man')
        base_build.run(self)
