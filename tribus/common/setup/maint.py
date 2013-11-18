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

import sys
import shutil
import os
from sphinx.application import Sphinx
from babel.messages.frontend import (extract_messages as base_extract_messages,
									 init_catalog as base_init_catalog,
									 update_catalog as base_update_catalog)

from tribus.config.base import DOCDIR
from tribus.common.utils import get_path, list_files, list_dirs

class extract_messages(base_extract_messages):

    def run(self):
    	base_extract_messages.run(self)

        srcdir = get_path([DOCDIR, 'rst'])
        outdir = get_path([DOCDIR, 'rst', 'i18n', 'pot'])
        doctreedir = get_path([DOCDIR, 'doctrees'])
        buildername = 'gettext'
        app = Sphinx(srcdir=srcdir, confdir=srcdir, outdir=outdir, doctreedir=doctreedir,
                     buildername=buildername, confoverrides=None, status=sys.stdout,
                     warning=sys.stderr, freshenv=True, warningiserror=False, tags=None)
        try:
            app.build(force_all=True)
        except Exception, e:
            print e

        try:
            shutil.rmtree(doctreedir)
        except Exception, e:
            print e


class init_catalog(base_init_catalog):

    def initialize_options(self):
        base_init_catalog.initialize_options(self)
        self.locale = 'en'

    def get_sphinx_pot_list(self):
        return filter(None, list_files(get_path([DOCDIR, 'rst', 'i18n', 'pot'])))

    def get_locale_list(self):

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
        from django.conf import settings
        print settings.LANGUAGES
        locales = list_dirs(get_path([DOCDIR, 'rst', 'i18n']))
        locales.remove('pot')
        return filter(None, locales)

    def run(self):
        for locale in self.get_locale_list():
            self.locale = locale
            self.output_file = None
            base_init_catalog.finalize_options(self)
            base_init_catalog.run(self)

            for potfile in self.get_sphinx_pot_list():
                self.locale = locale
                self.domain = os.path.splitext(os.path.basename(potfile))[0]
                self.output_dir = get_path([DOCDIR, 'rst', 'i18n'])
                self.input_file = potfile
                self.output_file = None
                base_init_catalog.finalize_options(self)
                base_init_catalog.run(self)


class update_catalog(base_update_catalog):

    def get_sphinx_pot_list(self):
        return filter(None, list_files(get_path([DOCDIR, 'rst', 'i18n', 'pot'])))

    def run(self):
        base_update_catalog.run(self)

        for potfile in self.get_sphinx_pot_list():
            self.domain = os.path.splitext(os.path.basename(potfile))[0]
            self.input_file = potfile
            self.output_dir = get_path([DOCDIR, 'rst', 'i18n'])
            base_update_catalog.finalize_options(self)
            base_update_catalog.run(self)