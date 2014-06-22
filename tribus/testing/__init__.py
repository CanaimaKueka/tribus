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

tribus.testing
==============

This file contains the entry point to the tribus tests.

"""

import sys
import os
import pep257
from unittest import TestSuite
from flake8.main import print_report
from flake8.engine import get_style_guide
from coverage import coverage
from coverage.misc import CoverageException
from coveralls import Coveralls
from coveralls.api import CoverallsException

from tribus import BASEDIR
from tribus.common.utils import find_files, get_path
from tribus.common.logger import get_logger
from tribus.config.pkg import exclude_packages
from tribus.common.setup.utils import get_packages

log = get_logger()


class SetupTesting(TestSuite):
    """

    Test Suite configuring Django settings and using DjangoTestSuiteRunner
    as test runner. Also runs PEP8 and Coverage checks.

    """

    def __init__(self, *args, **kwargs):
        self.configure()
        self.coverage = coverage()
        self.coverage.start()
        self.packages = get_packages(path=BASEDIR,
                                     exclude_packages=exclude_packages)
        self.options = {'failfast': True,
                        'autoreload': '',
                        'label': ['testing']}

        super(SetupTesting, self).__init__(tests=self.build_tests(),
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
        TODO: Cleanup/simplify this method, flow too complex,
        too much duplication.

        """

        from django.db.models import get_app
        from django.test.simple import build_suite

        return [build_suite(get_app('testing'))]

    def configure(self):
        """

        Configures Django settings.

        """

        from django.conf import settings
        from django.utils.importlib import import_module

        try:
            test_settings = import_module('tribus.config.testing')
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
        result = super(SetupTesting, self).run(result, *args, **kwargs)
        self.test_runner.teardown_databases(self.old_config)
        self.test_runner.teardown_test_environment()

        self.coverage_report()
        self.flake8_report()
        self.pep257_report()

        return result

    def flake8_report(self):
        """
        Outputs flake8 report.
        """
        log.info("\n\nFlake8 Report:")
        base = get_path([BASEDIR, 'tribus'])
        pys = find_files(path=base, pattern='*.py')
        flake8_style = get_style_guide()
        report = flake8_style.check_files(pys)
        print_report(report, flake8_style)

    def pep257_report(self):
        """
        Outputs flake8 report.
        """
        log.info("\n\nPEP257 Report:")
        base = get_path([BASEDIR, 'tribus'])
        pys = find_files(path=base, pattern='*.py')
        report = pep257.check(pys)

        if len(list(report)) > 0:
            for r in report:
                log.info(r)
        else:
            log.info("\nNo errors found!")

    def coverage_report(self):
        """
        Outputs Coverage report to screen and coverage.xml.
        """

        include = ['%s*' % package for package in self.packages]
        omit = ['*testing*']

        log.info("\n\nCoverage Report:")
        try:
            self.coverage.stop()
            self.coverage.report(include=include, omit=omit)
        except CoverageException as e:
            log.info("Coverage Exception: %s" % e)

        if os.environ.get('TRAVIS'):
            log.info("Submitting coverage to coveralls.io...")
            try:
                result = Coveralls()
                result.wear()
            except CoverallsException as e:
                log.error("Coveralls Exception: %s" % e)
