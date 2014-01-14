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


# import sys
# import os
# import inspect
# import argparse

# from tribus import BASEDIR
# from tribus.common.logger import get_logger
# from tribus.common.utils import find_files, package_to_path, get_path
# from tribus.common.commands import Helper
# from tribus.config.base import DEFAULT_CLI_OPTIONS

# log = get_logger()


# def find_tbs_subcommands(path, package):
#     _subcommands = []
#     _subcommands_dir = get_path([BASEDIR]+package_to_path(package).split(os.sep))
#     for pyfile in find_files(path=_subcommands_dir, pattern='*.py'):
#         pyname = os.path.basename(pyfile)
#         pymod = os.path.splitext(pyname)[0]
#         if pyname != '__init__.py':
#             try:
#                 module = vars(__import__(name=package,
# 												fromlist=[pymod]))[pymod]
#                 for item in vars(module).values():
#                     if inspect.isclass(item) and callable(item):
#                         if issubclass(item, Helper) and item != Helper:
#                             _subcommands.append(item)
#             except Exception, e:
#                 print e
#     return _subcommands


# def main():
#     """
#     Main command-line execution loop.
#     """
#     try:

#         parser = argparse.ArgumentParser(description='Tribus FTW',
#                                          epilog='Tribus END',
# 										   add_help=False, prog='Tribus')
#         for _args, _kwargs in DEFAULT_CLI_OPTIONS.values():
#             parser.add_argument(*_args, **_kwargs)

#         subparsers = parser.add_subparsers(title='subcommands',
# description='valid subcommands', help='additional help')

#         for cmd in find_tbs_subcommands(BASEDIR, 'tribus.cli.commands'):
#             subparser = subparsers.add_parser(
# 						cmd.helper_name,
# 						help=cmd.helper_help)
#             subparser.set_defaults(func=cmd)
#             for _args, _kwargs in cmd.helper_args.values():
#                 subparser.add_argument(*_args, **_kwargs)

#         args = parser.parse_args()

#         if args.print_help:
#             parser.print_help()
#         elif hasattr(args, 'func'):
#             args.func(args)
#         else:
#             parser.print_usage()

#     except SystemExit:
# a number of internal functions might raise this one.
#         raise
#     except KeyboardInterrupt:
#         sys.stderr.write("\nStopped.\n")
#         sys.exit(1)
#     except:
#         sys.excepthook(*sys.exc_info())
# we might leave stale threads if we don't explicitly exit()
#         sys.exit(1)
#     finally:
#         print 'end'
#     sys.exit(0)


# if __name__ == '__main__':
#     main()
