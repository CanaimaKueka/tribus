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

# from tribus.common.commands import Helper


# class Package(Helper):

#     helper_name = 'buildpackage'
#     helper_help = 'Helps build a package'
#     helper_args = {
#         'version': [['-v', '--version'], {
#             'action': 'store_true',
#             'dest': 'print_version',
#             'default': False
#         }],
#     }

#     helper_commands = {
#         'create': """


#         """,
#         'download': ,
#         'unpack': ,
#         'upload': ,
#         'describe': ,
#         'download': ,
#         'download': ,
#         'download': ,
#         'download': ,
#     }
#     package_dist = ['debian', 'fedora', 'python', 'ruby']
#     package_types = ['source', 'binary']
#     package_locations = ['local', 'remote']

#     def __init__(self, *args, **kwargs):
#         return self.run(*args, **kwargs)

#     def __call__(self, *args, **kwargs):
#         return self.run(*args, **kwargs)

#     def run(self, *args, **kwargs):
#         print self.subcommand_name
