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

"""Contains a representation of the configuration of a charm."""

import os
import stat
import zipfile
import tempfile

from tribus.common.charms.base import CharmBase, get_revision
from tribus.common.charms.bundle import CharmBundle
from tribus.common.charms.config import ConfigOptions
from tribus.common.charms.errors import InvalidCharmFile
from tribus.common.charms.metadata import MetaData


class CharmDirectory(CharmBase):

    """

    Directory that holds charm content.

    :param path: path to a charm directory.

    The directory must contain the following files::

    - ``metadata.yaml``

    """

    type = "dir"

    def __init__(self, path):
        """Set initial values and parse configuration files from the charm."""
        self.path = path
        revision_content = None
        self.metadata = MetaData(os.path.join(path, 'metadata.yaml'))
        revision_path = os.path.join(self.path, 'revision')

        if os.path.exists(revision_path):
            with open(revision_path) as f:
                revision_content = f.read()

        self._revision = get_revision(revision_content, self.metadata,
                                      self.path)

        if self._revision is None:
            self.set_revision(0)

        elif revision_content is None:
            self.set_revision(self._revision)

        self.config = ConfigOptions()
        self.config.load(os.path.join(path, 'config.yaml'))
        self._temp_bundle = None
        self._temp_bundle_file = None

    def get_revision(self):
        """Get charm revision from directory."""
        return self._revision

    def set_revision(self, revision):
        """Set charm revision of a directory representation."""
        self._revision = revision
        with open(os.path.join(self.path, 'revision'), 'w') as f:
            f.write(str(revision) + '\n')

    def make_archive(self, path):
        """

        Create an archive of the directory and write it to ``path``.

        :param path: path to archive.

        - build/* - This is used for packing the charm itself and any
                    similar tasks.
        - */.*    - Hidden files are all ignored for now.  This will most
                    likely be changed into a specific ignore list (.bzr, etc)

        """
        zf = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)

        for dirpath, dirnames, filenames in os.walk(self.path):
            relative_path = dirpath[len(self.path) + 1:]
            if relative_path and not self._ignore(relative_path):
                zf.write(dirpath, relative_path)
            for name in filenames:
                archive_name = os.path.join(relative_path, name)
                if not self._ignore(archive_name):
                    real_path = os.path.join(dirpath, name)
                    self._check_type(real_path)
                    if os.path.islink(real_path):
                        self._check_link(real_path)
                        self._write_symlink(
                            zf, os.readlink(real_path), archive_name)
                    else:
                        zf.write(real_path, archive_name)
        zf.close()

    def _check_type(self, path):
        """Check the path."""
        s = os.stat(path)

        if stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode):
            return path

        raise InvalidCharmFile(self.metadata.name, path,
                               'Invalid file type for a charm')

    def _check_link(self, path):
        """Check the path."""
        link_path = os.readlink(path)

        if link_path[0] == '/':
            raise InvalidCharmFile(self.metadata.name, path,
                                   'Absolute links are invalid')

        path_dir = os.path.dirname(path)
        link_path = os.path.join(path_dir, link_path)

        if not link_path.startswith(os.path.abspath(self.path)):
            raise InvalidCharmFile(self.metadata.name, path,
                                   'Only internal symlinks are allowed')

    def _write_symlink(self, zf, link_target, link_path):
        """Package symlinks with appropriate zipfile metadata."""
        info = zipfile.ZipInfo()
        info.filename = link_path
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0755) << 16
        zf.writestr(info, link_target)

    def _ignore(self, path):
        if path == 'build' or path.startswith('build/'):
            return True
        if path.startswith('.'):
            return True

    def as_bundle(self):
        if self._temp_bundle is None:
            prefix = '%s-%d.charm.' % (self.metadata.name, self.get_revision())
            temp_file = tempfile.NamedTemporaryFile(prefix=prefix)
            self.make_archive(temp_file.name)
            self._temp_bundle = CharmBundle(temp_file.name)
            self._temp_bundle_file = temp_file

        return self._temp_bundle

    def as_directory(self):
        return self

    def compute_sha256(self):
        """Compute sha256, based on the bundle."""
        return self.as_bundle().compute_sha256()
