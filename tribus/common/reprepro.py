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

tribus.common.reprepro
======================

This module contains functions to manage reprepro repositories.

'''

import os
import shutil
from fabric import local
from tribus.common.utils import list_items


def create_repository(repository_root, distributions_path):
    '''
    Creates and initializes a packages repository from a
    `distributions` configuration file.

    :param repository_root: path where the repository will be created.

    :param distributions_path: path to the `distributions` configuration file.
    '''

    conf_dir = os.path.join(repository_root, 'conf')
    dist_dst = os.path.join(conf_dir, 'distributions')

    if not os.path.isdir(repository_root):
        os.makedirs(conf_dir)

    shutil.copyfile(distributions_path, dist_dst)
    os.chdir(repository_root)
    local("reprepro -VVV export")

    with open(os.path.join(repository_root, 'distributions'), 'w') as f:
        for dist in list_items(os.path.join(repository_root, 'dists'), True, False):
            f.write('%s dists/%s/Release\n' % (dist, dist))


def include_deb(repository_root, distribution, comp=None, package_path=None):
    '''
    Indexes a debian package (.deb) in the selected repository.

    :param repository_root: path of the repository used.

    :param distribution: distribution where the package will be indexed.

    :param package_path: Either the path of a single .deb package or a directory with many .deb packages.
    '''

    # Esto puede ser un problema si despues se ejecuta otro proceso 
    # sin especificar la ubicacion
    os.chdir(repository_root)
    if os.path.isdir(package_path):
        local("reprepro -C %s includedeb %s %s/*.deb" % (comp, distribution, package_path))
    elif os.path.isfile(package_path):
        local('reprepro -C %s includedeb %s %s' % (comp, distribution, package_path))


def reset_repository(repository_root):
    '''
    Elimina las distribuciones existentes en un repositorio.
    '''

    os.chdir(repository_root)
    dists = list_items(os.path.join(repository_root, 'dists'), True, False)

    for dist in dists:
        local("reprepro removefilter %s \'Section\'" % dist)
