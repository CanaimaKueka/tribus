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

import os
from django.core.management.base import BaseCommand
from tribus.common.utils import list_items, find_files
from tribus.common.reprepro import include_deb
from tribus.config.pkgrecorder import LOCAL_ROOT, SAMPLES_DIR
from tribus.common.logger import get_logger
logger = get_logger()


class Command(BaseCommand):

    def handle(self, *args, **options):

        for dist in list_items(SAMPLES_DIR, True, False):
            for comp in list_items(os.path.join(SAMPLES_DIR, dist), True, False):
                for sample in find_files(os.path.join(SAMPLES_DIR, dist, comp)):
                    try:
                        include_deb(LOCAL_ROOT, dist, comp, sample)
                    except:
                        logger.info('There are no packages here!')
