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

tribus.common.recorder
======================

This module contains common functions to record package data from a repository.

'''

# NAMING CONVENTIONS MOSTLY BASED ON:
# https://www.debian.org/doc/debian-policy/ch-controlfields.html

import os
import re
import gzip
import urllib
import urllib2
import email.Utils
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from django.db.models import Q
from tribus.common.logger import get_logger
from tribus.web.cloud.models import Package, Details
from tribus.common.utils import find_files, md5Checksum,\
list_items, readconfig

logger = get_logger()

def record_paragraph(paragraph, branch):
    """
    Records the content of a paragraph in the database.

    :param paragraph: contains information about a binary package.

    :param branch: codename of the Canaima's version that will be recorded.

    .. versionadded:: 0.1
    """
    
    try:
        logger.info('Recording package \'%s\' into \'%s\' branch...'
                    % (paragraph['Package'], branch))
        package = Package.objects.create(paragraph)
        details = Details.objects.create(paragraph, package, branch)
        details.record_relations(details, paragraph.relations.items())
    except:
        logger.error('Could not record %s' % paragraph['Package'])


def update_paragraph(paragraph, branch):
    """
    Updates basic data and details of a package in the database.
    It also updates the package's relations.

    :param paragraph: contains information about a binary package.

    :param branch: codename of the Canaima's version that will be updated.

    .. versionadded:: 0.1
    """
    
    logger.info('Updating package \'%s\'' % paragraph['Package'])
    package = update_package(paragraph)
    details = update_details(package, paragraph, branch)
    for relation in details.Relations.all():
        details.Relations.remove(relation)
        exists = Details.objects.filter(Relations=relation)
        if not exists:
            relation.delete()
    record_relations(details, paragraph.relations.items())
    logger.info('Package \'%s\' successfully updated' % paragraph['Package'])
    

def create_cache(repository_root, cache_dir_path):
    '''
    Creates the cache and all other necessary directories to organize the
    control files pulled from the repository.

    :param repository_root: url of the repository from which the control files files will be pulled.
    
    :param cache_dir_path: path where the cache will be created.

    .. versionadded:: 0.1
    '''
    
    local_branches = (branch.split()
                      for branch in readconfig(os.path.join(repository_root,
                                                            "distributions")))
    for branch_name, branch_release_path in local_branches:
        release_path = os.path.join(repository_root, branch_release_path)
        try:
            md5list = deb822.Release(urllib.urlopen(release_path)).get('MD5sum')
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (branch_release_path, e.code))
        else:
            for control_file_data in md5list:
                if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$",
                            control_file_data['name']):
                    component, architecture, _ = control_file_data['name'].split("/")
                    local_path = os.path.join(cache_dir_path, branch_name,
                                              component, architecture)
                    remote_file = os.path.join(repository_root, "dists",
                                               branch_name,
                                               control_file_data['name'])
                    if not os.path.isdir(local_path):
                        os.makedirs(local_path)
                    f = os.path.join(local_path, "Packages.gz")
                    if not os.path.isfile(f):
                        try:
                            urllib.urlretrieve(remote_file, f)
                        except urllib2.URLError, e:
                            logger.error('Could not get %s, error code #%s' % (remote_file, e.code))
                    else:
                        if md5Checksum(f) != control_file_data['md5sum']:
                            os.remove(f)
                            try:
                                urllib.urlretrieve(remote_file, f)
                            except urllib2.URLError, e:
                                logger.error('Could not get %s, error code #%s' % (remote_file, e.code))


def update_cache(repository_root, cache_dir_path):
    '''
    Updates the control files existent in the cache,
    comparing the the ones in the repository with its local copies.
    If there are differences in the MD5sum field then the local
    copies are deleted and copied again from the repository. 
    It is assumed that the cache directory was created previously.
    
    :param repository_root: url of the repository from which the Packages files will be updated.

    :param cache_dir_path: path to the desired cache directory

    .. versionadded:: 0.1
    '''
    
    local_branches = (branch.split()
                      for branch in readconfig(os.path.join(repository_root,
                                                            "distributions")))
    for branch, _ in local_branches:
        remote_branch_path = os.path.join(repository_root, "dists", branch)
        local_branch_path = os.path.join(cache_dir_path, branch)
        release_path = os.path.join(remote_branch_path, "Release")
        try:
            md5list = deb822.Release(urllib.urlopen(release_path)).get('MD5sum')
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (remote_branch_path, e.code))
        else:
            for package_control_file in md5list:
                if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$",
                            package_control_file['name']):
                    _, architecture, _ = package_control_file['name'].split("/")
                    # BUSCAR UNA FORMA MENOS PROPENSA A ERRORES PARA HACER ESTO
                    architecture = architecture.split("-")[1]
                    remote_package_path = os.path.join(remote_branch_path, package_control_file['name'])
                    local_package_path = os.path.join(local_branch_path, package_control_file['name'])
                    if package_control_file['md5sum'] != md5Checksum(local_package_path):
                        os.remove(local_package_path)
                        urllib.urlretrieve(remote_package_path, local_package_path)
                        update_package_list(local_package_path, branch, architecture)
                    else:
                        logger.info('There are no changes in %s' % local_package_path)


def update_package_list(control_file_path, branch, architecture):
    """
    Updates all packages in a control file.
    If a package exists but the MD5sum field is different from the one
    stored in the database then it updates the package data fields.
    If the package doesn't exists then its created.
    If the package exists in the database but is not found in the control
    file then its deleted.

    :param control_file_path: path to the control file.

    :param branch: codename of the Canaima's version that will be updated.
    
    :param architecture: architecture of the packages present in the control file.

    .. versionadded:: 0.1
    """
    
    try:
        package_control_file = deb822.Packages.iter_paragraphs(gzip.open(control_file_path))
    except IOError, e:
        logger.warning('Could not read control file in %s, error code #%s' % (control_file_path, e))
    else:
        logger.info('Updating package list')
        existent_packages = []
        for paragraph in package_control_file:
            existent_packages.append(paragraph['Package'])
            exists = Details.objects.filter(package__Name=paragraph['Package'],
                                            Architecture=paragraph['Architecture'],
                                            Distribution=branch)
            if exists:
                if paragraph['md5sum'] != exists[0].MD5sum:
                    logger.info('The md5 checksum does not match in the package \'%s\':' % paragraph['Package'])
                    logger.info('\'%s\' != \'%s\' ' % (paragraph['md5sum'], exists[0].MD5sum))
                    update_paragraph(paragraph, branch)
            else:
                logger.info('Adding new details to \'%s\' package in \'%s\' branch...'  % (paragraph['package'], branch))
                record_paragraph(paragraph, branch)
    
        bd_packages = Package.objects.filter(Details__Distribution=branch).filter(Q(Details__Architecture='all') |
                                                                                  Q(Details__Architecture=architecture)).distinct()
        for package in bd_packages:
            if package.Name not in existent_packages:
                for detail in package.Details.all():
                    if detail.Distribution == branch and (detail.Architecture == architecture or detail.Architecture == 'all'):
                        for relation in detail.Relations.all():
                            detail.Relations.remove(relation)
                            exists = Details.objects.filter(Relations=relation)
                            if not exists:
                                relation.delete()
                        logger.info('Removing \'%s\' from \'%s\'...'
                                    % (detail, package.Name))
                        detail.delete()
                if not package.Details.all():
                    logger.info('Removing %s...' % package.Name)
                    package.delete()


def fill_db_from_cache(cache_dir_path):
    '''
    Records the data from each control file in the cache folder into the database.
    
    :param cache_dir_path: path where the package cache is stored.

    .. versionadded:: 0.1
    '''

    local_branches = filter(None, list_items(path=cache_dir_path, dirs=True, files=False))
    for branch in local_branches:
        dist_sub_paths = [os.path.dirname(f)
                          for f in find_files(os.path.join(cache_dir_path, branch), 'Packages.gz')]
        for path in dist_sub_paths:
            for p in find_files(path, "Packages.gz"):
                for paragraph in deb822.Packages.iter_paragraphs(gzip.open(p, 'r')):
                    record_paragraph(paragraph, branch)