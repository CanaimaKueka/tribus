#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.cmd import Command
from distutils.command.build import build as base_build
from docutils.core import Publisher
from docutils.writers import manpage
from sphinx.setup_command import BuildDoc as base_build_sphinx
from babel.messages.frontend import compile_catalog as base_compile_catalog

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.images import svg2png
from tribus.common.setup.utils import get_packages, get_package_data, get_data_files
from tribus.common.utils import get_path, find_files
from tribus.common.logger import get_logger
from tribus.config.pkg import (classifiers, long_description, install_requires, dependency_links,
                               exclude_packages, exclude_sources, exclude_patterns,
                               include_data_patterns, platforms, keywords)
log = get_logger()

import sys
from StringIO import StringIO

from sphinx.application import Sphinx
from sphinx.util.console import darkred, nocolor, color_terminal


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
    def run(self):
        if not color_terminal():
            # Windows' poor cmd box doesn't understand ANSI sequences
            nocolor()
        if not self.verbose:
            status_stream = StringIO()
        else:
            status_stream = sys.stdout
        confoverrides = {}
        if self.project:
             confoverrides['project'] = self.project
        if self.version:
             confoverrides['version'] = self.version
        if self.release:
             confoverrides['release'] = self.release
        if self.today:
             confoverrides['today'] = self.today
        app = Sphinx(self.source_dir, self.config_dir,
                     self.builder_target_dir, self.doctree_dir,
                     self.builder, confoverrides, status_stream,
                     freshenv=self.fresh_env)

        try:
            app.build(force_all=self.all_files)
        except Exception, err:
            from docutils.utils import SystemMessage
            if isinstance(err, SystemMessage):
                print >>sys.stderr, darkred('reST markup error:')
                print >>sys.stderr, err.args[0].encode('ascii',
                                                       'backslashreplace')
            else:
                raise

        if self.link_index:
            src = app.config.master_doc + app.builder.out_suffix
            dst = app.builder.get_outfilename('index')
            os.symlink(src, dst)


class compile_catalog(base_compile_catalog):
    def run(self):
        base_compile_catalog.run(self)


class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('compile_catalog')
        self.run_command('build_img')
        self.run_command('build_sphinx')
        self.run_command('build_man')
        base_build.run(self)