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
from tribus.web.cloud.models import Package, Details, Relation, Label, Tag,\
Maintainer
from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
from tribus.common.utils import find_files, md5Checksum,\
list_items, readconfig

logger = get_logger()

# Version alternativa de registro con manejo de excepciones en caso de errores.
# 
# @transaction.commit_manually
# def record_maintainer(maintainer_data):
#     """
#     Queries the database for an existent maintainer.
#     If it does not exists, it creates a new maintainer.
#   
#     :param maintainer_data: a string which contains maintainer's name and
#     email.
#   
#     :return: a `Maintainer` object.
#   
#     :rtype: ``Maintainer``
#   
#     .. versionadded:: 0.1
#     """
#       
#     maintainer_name, maintainer_mail = email.Utils.parseaddr(maintainer_data)
#       
#     try:
#         maintainer, _ = Maintainer.objects.get_or_create(Name=maintainer_name,
#                                                          Email=maintainer_mail)
#     except DatabaseError, e:
#         transaction.rollback()
#         logger.info("There has been an error recording %s" % (maintainer_data))
#         logger.error(e.message)
#     else:
#         transaction.commit()
#         return maintainer
    
    
def record_maintainer(maintainer_data):
    """
    Queries the database for an existent maintainer.
    If it does not exists, it creates a new maintainer.
  
    :param maintainer_data: a string which contains maintainer's name and
    email.
  
    :return: a `Maintainer` object.
  
    :rtype: ``Maintainer``
  
    .. versionadded:: 0.1
    """
    
    maintainer_name, maintainer_mail = email.Utils.parseaddr(maintainer_data)
    maintainer, _ = Maintainer.objects.get_or_create(Name=maintainer_name,
                                                      Email=maintainer_mail)
    return maintainer


def select_paragraph_data_fields(paragraph, data_fields):
    """
    Selects the necessary fields to record a control file
    in the database. Hyphens in field's names are suppressed, e.g:
    "Multi-Arch" is replaced by "MultiArch".

    :param paragraph: contains information about a binary package.

    :param data_fields: is a list of the necessary fields to record a Package or a Details object in the
                   database. For a `Package` object, the necessary fields are::

                        ["Package", "Description", "Homepage", "Section",
                         "Priority", "Essential", "Bugs", "Multi-Arch"]

                   and for a `Details` object::

                        ["Version", "Architecture", "Size", "MD5sum", "Filename",
                         "Installed-Size"]

    :return: a dictionary with the selected fields.

    :rtype: ``dict``

    .. versionadded:: 0.1
    """

    d = {}
    for data_field in data_fields:
        if data_field in paragraph:
            if "-" in data_field:
                d[data_field.replace("-", "")] = paragraph[data_field]
            else:
                d[data_field] = paragraph[data_field]
    return d


def record_package(paragraph):
    """
    Queries the database for an existent package.
    If the package does exists but it doesn't have
    a maintainer, then the package data will be
    updated acording to the fields of the paragraph provided.
    If the package doesn't exists then it's created.

    :param paragraph: contains information about a binary package.

    :return: a `Package` object.

    :rtype: ``Package``

    .. versionadded:: 0.1
    """
    
    exists = Package.objects.filter(Package=paragraph['Package'])
    if exists:
        if exists[0].Maintainer:
            return exists[0]
        else:
            exists.update(**select_paragraph_data_fields(paragraph, PACKAGE_FIELDS))
            package = Package.objects.filter(Package=paragraph['Package'])[0]
            package.Maintainer = record_maintainer(paragraph['Maintainer'])
            package.save()
            return package
    else:
        data_fields = select_paragraph_data_fields(paragraph, PACKAGE_FIELDS)
        maintainer = record_maintainer(paragraph['Maintainer'])
        package = Package(**data_fields)
        package.Maintainer = maintainer
        package.save()
        record_tags(paragraph, package)
        return package


def record_details(paragraph, package, branch):
    """
    Queries the database for the details of a given package.
    If there are no details then they are recorded.

    :param paragraph: contains information about a binary package.

    :param package: a `Package` object to which the details are related.

    :param branch: codename of the Canaima's version that will be recorded.

    :return: a `Details` object.

    :rtype: ``Details``

    .. versionadded:: 0.1
    """

    exists = Details.objects.filter(package=package,
                                    Architecture=paragraph['Architecture'],
                                    Distribution=branch)
    if exists:
        return exists[0]
    else:
        data_fields = select_paragraph_data_fields(paragraph, DETAIL_FIELDS)
        details = Details(**data_fields)
        details.Distribution = branch
        details.save()
        package.Details.add(details)
        return details


def record_tags(paragraph, package):
    """
    Processes the contents of the 'Tag' field in the provided paragraph,
    records the labels into the database and relates them to a package.

    :param paragraph: contains information about a binary package.

    :param package: a `Package` object to which the labels are related.

    .. versionadded:: 0.1
    """

    if 'Tag' in paragraph:
        tag_list = paragraph['Tag'].replace("\n", "").split(", ")
        for tag in tag_list:
            tag_name, tag_value = tag.split("::")
            value, _ = Tag.objects.get_or_create(Value=tag_value)
            label, _ = Label.objects.get_or_create(Name=tag_name, Tags=value)
            package.Labels.add(label)


def record_relationship(details, relation_type, fields, alt_id=0):
    """
    Records a new relation in the database and then associates it to a `Details` object.

    :param details: a `Details` object to which the relationship is related.

    :param relation_type: a string indicating the relationship type.

    :param fields: a dictionary which contains the relation information. Its structure is similar to::

                       {"name": "0ad-data", "version": (">=", "0~r11863"), "arch": None}

    :param alt_id: an integer used to relate a relation with its alternatives, e.g:

                       +----+-----------------+---------------+-----------+---------+--------+
                       | id | related_package | relation_type | relation  | version | alt_id |
                       +====+=================+===============+===========+=========+========+
                       |  1 |       23        |     depends   |    <=     |  0.98   |        |
                       +----+-----------------+---------------+-----------+---------+--------+
                       |  2 |       24        |     depends   |    >=     |  0.64   |    1   |
                       +----+-----------------+---------------+-----------+---------+--------+
                       |  3 |       25        |     depends   |    >=     |  2.76   |    1   |
                       +----+-----------------+---------------+-----------+---------+--------+
                       |  4 |       26        |     depends   |           |         |    1   |
                       +----+-----------------+---------------+-----------+---------+--------+
                       |  5 |       27        |     depends   |    <<     |  2.14   |        |
                       +----+-----------------+---------------+-----------+---------+--------+

                    in the above table, the relations with id 2, 3 and 4 are alternatives between
                    themselves because they have the same value in the field `alt_id`.

    .. versionadded:: 0.1
    """
    
    version = fields.get('version', None) 
    if version:
        relation_version, number_version = version
    else:
        relation_version, number_version = (None, None)
    related_package, _ = Package.objects.get_or_create(Package=fields['name'])
    new_relation, _ = Relation.objects.get_or_create(**{"related_package": related_package,
                                        "relation_type": relation_type,
                                        "relation": relation_version,
                                        "version": number_version,
                                        "alt_id": alt_id})
    details.Relations.add(new_relation)


def record_relations(details, relations_list):
    """
    Records a set of relations associated to a `Details` object.

    :param details: a `Details` object to which each relationship is related.

    :param relations_list: a list of tuples containing package relations to another packages.
                      Its structure is similar to::

                          [('depends', [[{'arch': None, 'name': u'libgl1-mesa-glx', 'version': None},
                          {'arch': None, 'name': u'libgl1', 'version': None}]],
                          [{'arch': None, 'name': u'0ad-data', 'version': (u'>=', u'0~r11863')}]), ('suggests', [])]

    .. versionadded:: 0.1
    """
    
    for relation_type, relations in relations_list:
        alt_id = 1
        if relations:
            for relation in relations:
                if len(relation) > 1:
                    for relation_element in relation:
                        record_relationship(details, relation_type,
                                            relation_element, alt_id)
                    alt_id += 1
                else:
                    record_relationship(details, relation_type, relation[0])


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
        package = record_package(paragraph)
        details = record_details(paragraph, package, branch)
        record_relations(details, paragraph.relations.items())
    except:
        logger.error('Could not record %s' % paragraph['Package'])


def update_package(paragraph):
    """
    Updates the basic data of a package in the database.

    :param paragraph: contains information about a binary package.

    :return: a `Package` object.

    :rtype: ``Package``

    .. versionadded:: 0.1
    """

    package = Package.objects.get(Package=paragraph['Package'])
    for field, value in select_paragraph_data_fields(paragraph, PACKAGE_FIELDS).items():
        setattr(package, field, value)
    if not package.Maintainer:
        package.Maintainer = record_maintainer(paragraph['Maintainer'])
    package.save()
    return package


def update_details(package, paragraph, branch):
    """
    Updates the details of a Package in the database.

    :param package: a `Package` object to which the details are related.

    :param paragraph: contains information about a binary package.

    :param branch: codename of the Canaima's version that will be updated.

    :return: a `Details` object.

    :rtype: ``Details``

    .. versionadded:: 0.1
    """
    
    details = Details.objects.get(package=package,
                                  Architecture=paragraph['Architecture'],
                                  Distribution=branch)
    for field, value in select_paragraph_data_fields(paragraph, DETAIL_FIELDS).items():
        setattr(details, field, value)
    details.save()
    return details


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
            exists = Details.objects.filter(package__Package=paragraph['Package'],
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
            if package.Package not in existent_packages:
                for detail in package.Details.all():
                    if detail.Distribution == branch and (detail.Architecture == architecture or detail.Architecture == 'all'):
                        for relation in detail.Relations.all():
                            detail.Relations.remove(relation)
                            exists = Details.objects.filter(Relations=relation)
                            if not exists:
                                relation.delete()
                        logger.info('Removing \'%s\' from \'%s\'...'
                                    % (detail, package.Package))
                        detail.delete()
                if not package.Details.all():
                    logger.info('Removing %s...' % package.Package)
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