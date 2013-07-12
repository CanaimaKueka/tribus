#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.install_data import install_data as base_install_data

from tribus.config.base import BASEDIR
from tribus.common.utils import get_data_files
from tribus.common.logger import get_logger
from tribus.config.pkg import exclude_sources, exclude_patterns, include_data_patterns

log = get_logger()

class install_data(base_install_data):
    def finalize_options(self):
        base_install_data.finalize_options(self)
        self.data_files = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                                         exclude_files=exclude_sources+exclude_patterns)

