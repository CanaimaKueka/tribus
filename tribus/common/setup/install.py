#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.install_data import install_data as base_install_data
from distutils.command.build_py import build_py as base_build_py

from tribus.config.base import BASEDIR
from tribus.common.setup.utils import get_data_files, get_packages, get_package_data
from tribus.common.logger import get_logger
from tribus.config.pkg import exclude_sources, exclude_patterns, include_data_patterns, exclude_packages

log = get_logger()

class build_py(base_build_py):
    def finalize_options(self):
        base_build_py.finalize_options(self)
    	data = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                              exclude_files=exclude_sources+exclude_patterns)
    	self.package_data = get_package_data(path=BASEDIR, packages=self.packages,
    										 data_files=data, exclude_files=exclude_sources+exclude_patterns,
		                                     exclude_packages=exclude_packages)
    	self.data_files = self.get_data_files()


class install_data(base_install_data):
    def finalize_options(self):
        base_install_data.finalize_options(self)
        self.data_files = get_data_files(path=BASEDIR, patterns=include_data_patterns,
                                         exclude_files=exclude_sources+exclude_patterns)