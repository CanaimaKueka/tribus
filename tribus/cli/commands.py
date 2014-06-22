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

# from ..common.cmd import Command


# class UpdateMirror(Command):

#     def __init__(self):
#         self.cmd = 'debmirror'
#         self.mirror_host = mirror_host
#         self.mirror_archs = mirror_archs
#         self.mirror_dir = mirror_dir
#         self.mirror_suites = mirror_suites
#         self.args = ['--source', '--host', self.mirror_host, '--method',
#                      'rsync', '--dist', self.mirror_suites, '--arch', self.mirror_archs,
#                      '--ignore-release-gpg', self.mirror_dir]
#         Command.__init__(self, cmd=self.cmd, args=self.args)
#         self.run_error = 'Couldn\'t remove "%s"' % self.tree


# class DpkgSourceExtract(Command):

#     """
#     Wrap dpkg-source to extract a Debian source package into a certain
#     directory, this needs
#     """

#     def __init__(self):
#         Command.__init__(self, 'dpkg-source', ['-x'])

#     def __call__(self, dsc, output_dir):
#         self.run_error = 'Couldn\'t extract "%s"' % dsc
#         Command.__call__(self, [dsc, output_dir])
