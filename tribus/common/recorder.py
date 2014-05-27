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
import logging
import email.Utils
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from tribus import BASEDIR
from django.db.models import Q
from tribus.common.logger import get_logger
from tribus.web.cloud.models import Package, Details
from tribus.common.utils import md5Checksum, list_items, readconfig

logger = get_logger()
hdlr = logging.FileHandler(os.path.join(BASEDIR, 'tribus_recorder.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def update_paragraph(paragraph, branch, comp):
    """
    Updates basic data and details of a package in the database.
    It also updates the package's relations.

    :param paragraph: contains information about a binary package.

    :param branch: codename of the Canaima's version that will be updated.
    
    :param comp: component to which the paragraph belongs.

    .. versionadded:: 0.1
    """
    
    logger.info('Updating package \'%s\' in %s:%s' %
                (paragraph['Package'], branch, comp))
    package = Package.objects.get(Name = paragraph.get('Package'))
    package.update(paragraph, branch, comp)
    logger.info('Package \'%s\' successfully updated in %s:%s'
                % (paragraph['Package'], branch, comp))


def create_cache(repository_root, cache_dir_path):
    '''
    Creates the cache and all other necessary directories to organize the
    control files pulled from the repository.

    :param repository_root: url of the repository from which the control files files will be pulled.
    
    :param cache_dir_path: path where the cache will be created.

    .. versionadded:: 0.1
    '''
    
    if not os.path.isdir(cache_dir_path):
        os.makedirs(cache_dir_path)
    
    branches = (branch.split()
                for branch in readconfig(os.path.join(repository_root,
                                                      "distributions")))
    for name, release_path in branches:
        release_path = os.path.join(repository_root, release_path)
        try:
            md5list = deb822.Release(urllib.urlopen(release_path)).get('MD5sum')
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (release_path, e.code))
        else:
            for control_file_data in md5list:
                if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", control_file_data['name']):
                    component, architecture, _ = control_file_data['name'].split("/")
                    remote_file = os.path.join(repository_root, "dists",
                                               name, control_file_data['name'])
                    local_name = "_".join([name, component,
                                           architecture.replace("binary-", "")])
                    f = os.path.join(cache_dir_path, local_name + ".gz")
                    
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


def sync_cache(repository_root, cache_dir_path):
    '''
    Synchronizes the existing control files in the cache,
    comparing the the ones in the repository with the local copies.
    If there are differences in the MD5sum field then the local
    copies are deleted and copied again from the repository.
    It is assumed that the cache directory was created previously.
    
    :param repository_root: url of the repository from which the Packages files will be updated.

    :param cache_dir_path: path to the desired cache directory

    .. versionadded:: 0.1
    '''
    
    branches = (branch.split()
                for branch in readconfig(os.path.join(repository_root,
                                                      "distributions")))
    changes = []
    for branch, _ in branches:
        remote_branch_path = os.path.join(repository_root, "dists", branch)
        release_path = os.path.join(remote_branch_path, "Release")
        try:
            md5list = deb822.Release(urllib.urlopen(release_path)).get('MD5sum')
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (remote_branch_path, e.code))
        else:
            for package_control_file in md5list:
                if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", package_control_file['name']):
                    component, architecture, _ = package_control_file['name'].split("/")
                    remote_package_path = os.path.join(remote_branch_path, package_control_file['name'])
                    local_name = "_".join([branch, component,
                                           architecture.replace("binary-", "")])
                    f = os.path.join(cache_dir_path, local_name + ".gz")
                    if package_control_file['md5sum'] != md5Checksum(f):
                        if os.path.exists(f):
                            os.remove(f)
                        try:
                            urllib.urlretrieve(remote_package_path, f)
                            changes.append(f)
                        except urllib2.URLError, e:
                            logger.error('Could not get %s, error code #%s' % (remote_package_path, e.code))
                    else:
                        logger.info('There are no changes in %s' % f)
    return changes


def update_db_from_cache(changes, cache_dir_path=None):
    """
    Updates all packages in a control file.
    If a package exists but the MD5sum field is different from the one
    stored in the database then it updates the package data fields.
    If the package doesn't exists then its created.
    If the package exists in the database but is not found in the control
    file then its deleted.
    
    :param cache_dir_path: path to the desired cache directory
    
    .. versionadded:: 0.1
    """
    
    if cache_dir_path:
        control_files = list_items(cache_dir_path, False, True)
    else:
        control_files = changes
    for control_file in control_files:
        name, _ = control_file.split(".")
        branch, comp, arch = name.split("_")
        path = os.path.join(cache_dir_path, control_file)
        try:
            paragraphs = deb822.Packages.iter_paragraphs(gzip.open(path))
        except IOError, e:
            logger.warning('Could not read control file in %s, error code #%s' % (path, e))
        else:
            logger.info('=====================')
            logger.info('Updating packages in %s:%s:%s' % (branch, comp, arch))
            existent_packages = []
            for paragraph in paragraphs:
                existent_packages.append(paragraph['Package'])
                exists = Details.objects.filter(package__Name=paragraph['Package'],
                                                Architecture=paragraph['Architecture'],
                                                Distribution=branch, 
                                                Component = comp)
                if exists:
                    if paragraph['md5sum'] != exists[0].MD5sum:
                        logger.info('The md5 checksum does not match in the package \'%s\':' % paragraph['Package'])
                        logger.info('\'%s\' != \'%s\' ' % (paragraph['md5sum'], exists[0].MD5sum))
                        update_paragraph(paragraph, branch, comp)
                    else:
                        logger.info('Nothing to change \'%s\':' % paragraph['Package'])
                else:
                    try:
                        Package.objects.create_auto(paragraph, branch, comp)
                    except:
                        logger.error('Could not record %s' % paragraph['Package'])
            
            bd_packages = Package.objects.filter(Details__Distribution=branch,
                                                 Details__Component = comp
                                                 ).filter(Q(Details__Architecture='all') |
                                                          Q(Details__Architecture=arch)).distinct()
            for package in bd_packages:
                if package.Name not in existent_packages:
                    print package.Name, "not in %s %s %s" % (branch, comp, arch)
                    for detail in package.Details.all():
                        if (detail.Distribution == branch and detail.Component == comp and
                            (detail.Architecture == arch or detail.Architecture == 'all')):
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
    
    control_files = list_items(cache_dir_path, False, True)
    for control_file in control_files:
        name, _ = control_file.split(".")
        branch, comp, _ = name.split("_")
        control_file_path = os.path.join(cache_dir_path, control_file)
        for paragraph in deb822.Packages.iter_paragraphs(gzip.open(control_file_path, 'r')):
            try:
                Package.objects.create_auto(paragraph, branch, comp)
            except:
                logger.error('Could not record %s' % paragraph['Package'])
