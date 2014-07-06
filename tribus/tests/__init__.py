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

This file contains the entry point to the tribus tests.

"""

import sys
from unittest import TestSuite

from tribus import BASEDIR
from tribus.common.logger import get_logger
from tribus.config.pkg import exclude_packages
from tribus.common.setup.utils import get_packages

log = get_logger()


class SetupTests(TestSuite):

    """

    This is the Test Suite of Tribus.

    Test Suite configuring Django settings and using DjangoTestSuiteRunner
    as test runner. Also runs Flake8, PEP257 and Coverage checks.

    """

    def __init__(self, *args, **kwargs):
        self.configure()
        self.packages = get_packages(path=BASEDIR,
                                     exclude_packages=exclude_packages)
        self.options = {'failfast': True,
                        'autoreload': '',
                        'label': ['tests']}

        super(SetupTests, self).__init__(tests=self.build_tests(),
                                         *args, **kwargs)

        # Setup testrunner.
        from django.test.simple import DjangoTestSuiteRunner
        self.test_runner = DjangoTestSuiteRunner(verbosity=2,
                                                 interactive=False,
                                                 failfast=True)

        # South patches the test management command to handle the
        # SOUTH_TESTS_MIGRATE setting. Apply that patch if South is installed.
        try:
            from south.management.commands import patch_for_test_db_setup
            patch_for_test_db_setup()
        except ImportError:
            pass

        self.test_runner.setup_test_environment()
        self.old_config = self.test_runner.setup_databases()

    def build_tests(self):
        """
        Build tests for inclusion in suite from resolved packages.
        """
        from django.db.models import get_app
        from django.test.simple import build_suite

        return [build_suite(get_app('tests'))]

    def configure(self):
        """
        Configures Django settings.

        """

        from django.conf import settings
        from django.utils.importlib import import_module

        try:
            test_settings = import_module('tribus.config.tests')
        except ImportError as e:
            log.info('ImportError: Unable to import test settings: %s' % e)
            sys.exit(1)

        setting_attrs = {}
        for attr in dir(test_settings):
            if '__' not in attr:
                setting_attrs[attr] = getattr(test_settings, attr)

        if not settings.configured:
            settings.configure(**setting_attrs)

    def run(self, result, *args, **kwargs):
        """

        Run the test, teardown the environment and generate reports.

        """

        result.failfast = self.options['failfast']
        result = super(SetupTests, self).run(result, *args, **kwargs)
        self.test_runner.teardown_databases(self.old_config)
        self.test_runner.teardown_test_environment()

        return result