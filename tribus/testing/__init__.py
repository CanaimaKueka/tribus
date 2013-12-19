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

tribus.testing
==============

This file contains the entry point to the tribus tests.

'''

# import sys
# from flake8.engine import get_parser, get_style_guide
# from flake8.util import is_flag, flag_on
# from coverage import coverage
# from coverage.misc import CoverageException
# from six import StringIO
# from unittest import TestSuite

# from tribus import BASEDIR
# from tribus.common.utils import get_logger
# from tribus.config.pkg import exclude_packages
# from tribus.common.setup.utils import get_packages

# log = get_logger()


# class SetupTesting(TestSuite):
#     """
#     Test Suite configuring Django settings and using
#     DjangoTestSuiteRunner as test runner.
#     Also runs PEP8 and Coverage checks.
#     """
#     def __init__(self, *args, **kwargs):
#         self.configure()
#         self.coverage = coverage()
#         self.coverage.start()
#         self.packages = get_packages(path=BASEDIR, exclude_packages=exclude_packages)
#         self.options = {
#             'failfast': '',
#             'autoreload': '',
#             'label': ['testing'],
#             }

#         super(SetupTesting, self).__init__(tests=self.build_tests(),
#                 *args, **kwargs)

#         # Setup testrunner.
#         from django.test.simple import DjangoTestSuiteRunner
#         self.test_runner = DjangoTestSuiteRunner(
#             verbosity=1,
#             interactive=False,
#             failfast=True
#         )
#         # South patches the test management command to handle the
#         # SOUTH_TESTS_MIGRATE setting. Apply that patch if South is installed.
#         try:
#             from south.management.commands import patch_for_test_db_setup
#             patch_for_test_db_setup()
#         except ImportError:
#             pass
#         self.test_runner.setup_test_environment()
#         self.old_config = self.test_runner.setup_databases()


#     def flake8_report(self):
#         """
#         Outputs flake8 report.
#         """
#         DEFAULT_CONFIG = os.path.join(
#             os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
#             'flake8'
#         )
#         # Hook into stdout.
#         old_stdout = sys.stdout
#         sys.stdout = mystdout = StringIO()

#         # Run Pep8 checks, excluding South migrations.
#         flake8_style = get_style_guide(config_file=DEFAULT_CONFIG,
#                                        **self.options_dict)
#         paths = self.distribution_files()
#         report = flake8_style.check_files(paths)
#         exit_code = print_report(report, flake8_style)
#         raise SystemExit(exit_code > 0)

#         # Restore stdout.
#         sys.stdout = old_stdout

#         # Return Pep8 result
#         log.info("\nPEP8 Report:")
#         log.info(mystdout.getvalue())


#     def coverage_report(self):
#         """
#         Outputs Coverage report to screen and coverage.xml.
#         """

#         log.info("\nCoverage Report:")
#         try:
#             include = ['%s*' % package for package in self.packages]
#             omit = ['*testing*']
#             self.coverage.report(include=include, omit=omit)
#         except CoverageException as e:
#             log.info("Coverage Exception: %s" % e)


#     def build_tests(self):
#         """
#         Build tests for inclusion in suite from resolved packages.
#         TODO: Cleanup/simplify this method, flow too complex,
#         too much duplication.
#         """
#         from django.db.models import get_app
#         from django.test.simple import build_suite

#         tests = []
#         app = get_app(self.options['label'][0])
#         tests.append(build_suite(app))

#         return tests

#     def configure(self):
#         """
#         Configures Django settings.
#         """
#         from django.conf import settings
#         from django.utils.importlib import import_module

#         try:
#             test_settings = import_module('tribus.config.testing')
#         except ImportError as e:
#             log.info('ImportError: Unable to import test settings: %s' % e)
#             sys.exit(1)

#         setting_attrs = {}
#         for attr in dir(test_settings):
#             if '__' not in attr:
#                 setting_attrs[attr] = getattr(test_settings, attr)

#         if not settings.configured:
#             settings.configure(**setting_attrs)

#     def run(self, result, *args, **kwargs):
#         """
#         Run the test, teardown the environment and generate reports.
#         """
#         result.failfast = self.options['failfast']
#         result = super(SetupTesting, self).run(result, *args, **kwargs)
#         self.test_runner.teardown_databases(self.old_config)
#         self.test_runner.teardown_test_environment()
#         self.coverage_report()
#         self.flake8_report()
#         return result



# class Flake8Command(setuptools.Command):
#     """The :class:`Flake8Command` class is used by setuptools to perform
#     checks on registered modules.
#     """

#     description = "Run flake8 on modules registered in setuptools"
#     user_options = []

#     def initialize_options(self):
#         self.option_to_cmds = {}
#         parser = get_parser()[0]
#         for opt in parser.option_list:
#             cmd_name = opt._long_opts[0][2:]
#             option_name = cmd_name.replace('-', '_')
#             self.option_to_cmds[option_name] = cmd_name
#             setattr(self, option_name, None)

#     def finalize_options(self):
#         self.options_dict = {}
#         for (option_name, cmd_name) in self.option_to_cmds.items():
#             if option_name in ['help', 'verbose']:
#                 continue
#             value = getattr(self, option_name)
#             if value is None:
#                 continue
#             if is_flag(value):
#                 value = flag_on(value)
#             self.options_dict[option_name] = value

#     def distribution_files(self):
#         if self.distribution.packages:
#             package_dirs = self.distribution.package_dir or {}
#             for package in self.distribution.packages:
#                 pkg_dir = package
#                 if package in package_dirs:
#                     pkg_dir = package_dirs[package]
#                 elif '' in package_dirs:
#                     pkg_dir = package_dirs[''] + os.path.sep + pkg_dir
#                 yield pkg_dir.replace('.', os.path.sep)

#         if self.distribution.py_modules:
#             for filename in self.distribution.py_modules:
#                 yield "%s.py" % filename

#     def run(self):
#         flake8_style = get_style_guide(config_file=DEFAULT_CONFIG,
#                                        **self.options_dict)
#         paths = self.distribution_files()
#         report = flake8_style.check_files(paths)
#         exit_code = print_report(report, flake8_style)
#         raise SystemExit(exit_code > 0)