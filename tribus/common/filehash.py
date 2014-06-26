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

This is an implementation of logging.config.dictConfig.

This implementation is backported from Python 2.7 for use in previous versions.

"""


def compute_file_hash(hash_type, filename):
    """

    Simple helper to compute the digest of a file.

    :param hash_type: A class like ``hashlib.sha256``.
    :param filename: File path to compute the digest from.
    :return: The file hash.

    .. versionadded:: 0.2

    """
    hash = hash_type()

    with open(filename) as file:
        # Chunk the digest extraction to avoid loading large
        # files in memory unnecessarily.
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hash.update(chunk)

    return hash.hexdigest()
