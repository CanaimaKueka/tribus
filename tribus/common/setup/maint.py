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

tribus.common.setup.maint
=========================


'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

import sys
import shutil
from django.conf import settings
from sphinx.application import Sphinx
from sphinx.builders.htmlhelp import chm_locales
from babel import Locale
from babel.localedata import locale_identifiers
from babel.messages.frontend import (extract_messages as base_extract_messages,
                                     init_catalog as base_init_catalog,
                                     update_catalog as base_update_catalog)

from tribus.config.base import BASEDIR, DOCDIR
from tribus.common.utils import get_path, list_files


class extract_messages(base_extract_messages):

    def run(self):
        base_extract_messages.run(self)

        srcdir = get_path([DOCDIR, 'rst'])
        outdir = get_path([DOCDIR, 'rst', 'i18n', 'pot'])
        doctreedir = get_path([DOCDIR, 'doctrees'])
        buildername = 'gettext'
        app = Sphinx(
            srcdir=srcdir, confdir=srcdir, outdir=outdir, doctreedir=doctreedir,
            buildername=buildername, confoverrides=None, status=sys.stdout,
            warning=sys.stderr, freshenv=True, warningiserror=False, tags=None)
        try:
            app.build(force_all=True)
        except Exception as e:
            print e

        try:
            shutil.rmtree(doctreedir)
        except Exception as e:
            print e


class init_catalog(base_init_catalog):

    def initialize_options(self):
        base_init_catalog.initialize_options(self)
        self.locale = 'en'

    def get_sphinx_pot_list(self):
        return filter(None, list_files(get_path([DOCDIR, 'rst', 'i18n', 'pot'])))

    def get_locale_list(self):
        django_locales = set([i[0].replace('_', '-').lower()
                             for i in settings.LANGUAGES])
        babel_locales = set([j.replace('_', '-').lower()
                            for j in locale_identifiers()])
        sphinx_locales = set([k.replace('_', '-').lower()
                             for k in chm_locales.keys()])
        locales = [str(Locale.parse(identifier=l, sep='-'))
                   for l in django_locales & babel_locales & sphinx_locales]
        return filter(None, locales)

    def run(self):
        for locale in self.get_locale_list():
            self.locale = locale
            self.domain = 'django'
            self.output_dir = get_path([BASEDIR, 'tribus', 'data', 'i18n'])
            self.input_file = get_path(
                [BASEDIR,
                 'tribus',
                 'data',
                 'i18n',
                 'pot',
                 'django.pot'])
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
