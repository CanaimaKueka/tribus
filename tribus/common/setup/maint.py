import sys
import shutil
import os
from sphinx.application import Sphinx
from babel.messages.frontend import (extract_messages as base_extract_messages,
									 init_catalog as base_init_catalog,
									 update_catalog as base_update_catalog)

from tribus.config.base import DOCDIR
from tribus.common.utils import get_path, list_files

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
    def run(self):
    	base_init_catalog.run(self)


class update_catalog(base_update_catalog):

    def get_sphinx_pot_list(self):
        return filter(None, list_files(get_path([DOCDIR, 'rst', 'i18n', 'pot'])))

    def run(self):
        base_update_catalog.run(self)

        for potfile in self.get_sphinx_pot_list():
            base_update_catalog.initialize_options(self)
            self.domain = os.path.splitext(os.path.basename(potfile))[0]
            self.input_file = potfile
            self.output_dir = get_path([DOCDIR, 'rst', 'i18n'])
            base_update_catalog.run(self)