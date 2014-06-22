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

tribus.common.iosync
====================

This module contains common OS functions coupled with a OS ``sync()`` call to
ensure that everything gets written to disk synchronously.

"""

import os


def sync():
    try:
        getattr(os, 'sync')
    except Exception:
        import sh
        os.sync = sh.sync
    finally:
        os.sync()


def makedirs(path=None):
    os.makedirs(path)
    sync()


def rmtree(path=None):
    import shutil
    shutil.rmtree(path)
    sync()


def touch(path=None):
    open(path, 'w').close()
    sync()


def ln(source=None, dest=None):
    os.symlink(source, dest)
    sync()
