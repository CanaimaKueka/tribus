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

Contains a representation of a bundle charm.

CharmBundle is a representation of a ZIP file containing a Charm.

"""

import hashlib
import tempfile
import os
import stat

from zipfile import ZipFile, BadZipfile

from tribus.common.charms.base import CharmBase, get_revision
from tribus.common.charms.config import ConfigOptions
from tribus.common.charms.metadata import MetaData
from tribus.common.charms.directory import CharmDirectory
from tribus.common.errors import CharmError
from tribus.common.filehash import compute_file_hash


class CharmBundle(CharmBase):

    """ZIP-archive that contains charm directory content."""

    type = 'bundle'

    def __init__(self, path):
        """Set initial values and parse configuration files from the charm."""
        self.path = isinstance(path, file) and path.name or path

        try:
            zf = ZipFile(path, 'r')
        except BadZipfile, exc:
            raise CharmError(path, 'must be a zip file (%s)' % exc)

        if 'metadata.yaml' not in zf.namelist():
            raise CharmError(path, ('charm does not contain required'
                                    ' file "metadata.yaml"'))

        self.metadata = MetaData()
        self.metadata.parse(zf.read('metadata.yaml'))

        try:
            revision_content = zf.read('revision')
        except KeyError:
            revision_content = None

        self._revision = get_revision(revision_content, self.metadata,
                                      self.path)

        if self._revision is None:
            raise CharmError(self.path, 'has no revision')

        self.config = ConfigOptions()

        if 'config.yaml' in zf.namelist():
            self.config.parse(zf.read('config.yaml'))

    def get_revision(self):
        """Get charm revision from bundle."""
        return self._revision

    def compute_sha256(self):
        """

        Return the SHA256 digest for this charm bundle.

        The digest is extracted out of the final bundle file itself.

        """
        return compute_file_hash(hashlib.sha256, self.path)

    def extract_to(self, directory_path):
        """Extract the bundle to folder and return a CharmDirectory handle."""
        zf = ZipFile(self.path, 'r')

        for info in zf.infolist():

            mode = info.external_attr >> 16

            if stat.S_ISLNK(mode):
                source = zf.read(info.filename)
                target = os.path.join(directory_path, info.filename)

                if os.path.exists(target):
                    os.remove(target)

                os.symlink(source, target)
                continue

            extract_path = zf.extract(info, directory_path)
            os.chmod(extract_path, mode)

        return CharmDirectory(directory_path)

    def as_bundle(self):
        """Return the bundle as a CharmBundle instance."""
        return self

    def as_directory(self):
        """Return the bundle as a CharmDirectory using a temporary path."""
        dn = tempfile.mkdtemp(prefix="tmp-charm-")
        return self.extract_to(dn)
