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

from django.core.management.base import BaseCommand
from tribus.common.utils import list_items, find_files
from tribus.common.reprepro import include_deb


class Command(BaseCommand):

    def handle(self, *args, **options):
        dirs = [os.path.dirname(f)
                for f in find_files(env.sample_packages_dir, 'list')]
        dists = filter(None, list_items(env.sample_packages_dir, dirs=True, files=False))
        with cd('%(reprepro_dir)s' % env):
            for directory in dirs:
                # No se me ocurre una mejor forma (dinamica) de hacer esto
                dist = [dist_name for dist_name in dists if dist_name in directory][0]
                results = [each for each in os.listdir(directory) if each.endswith('.deb')]
                if results:
                    include_deb(env.reprepro_dir, dist, directory)
                else:
                    logger.info('There are no packages in %s' % directory)
