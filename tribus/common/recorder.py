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

#===============================================================================
# TODO: 
# 1. Actualizacion de tags. PENDIENTE
# 2. Parece necesario y correcto sustituir el None de las relacione simples por 0. PENDIENTE
# 3. Eliminar paquetes obsoletos durante las actualizaciones. Actualmente no elimina los paquetes que ya
#     se registraron. PENDIENTE
#===============================================================================

import urllib, re, email.Utils, os, sys, string, random
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from tribus.web.cloud.models import *
from tribus.config.pkgrecorder import package_fields, detail_fields, LOCAL_ROOT, CANAIMA_ROOT
from tribus.common.utils import find_files, md5Checksum, find_dirs, scan_repository,\
    list_dirs
from tribus.config.base import PACKAGECACHE
from tribus.config.web import DEBUG
from django.db.models import Q


def record_maintainer(maintainer_data):
    """
    Queries the database for an existent maintainer.
    If it does not exists, it creates a new maintainer.
    
    :param maintainer_data: a string which contains maintainer's name and email.
    
    :return: a `Maintainer` object.
             
    :rtype: ``Maintainer``
    
    .. versionadded:: 0.1
    """
    name, mail = email.Utils.parseaddr(maintainer_data)
    exists = Maintainer.objects.filter(Name = name, Email = mail)
    if not exists:
        m = Maintainer(Name = name, Email = mail)
        m.save()
        return m
    else:
        return exists[0]


def select_paragraph_fields(section, fields):
    """
    Selects the necessary fields to record a debian control file paragraph
    in the database. Hyphens in field's names are suppressed, e.g:  
    "Multi-Arch" is replaced by "MultiArch".
    
    :param section: is a paragraph which contains data from a binary package.
    
    :param fields: is a list of the necessary fields to record a Package or a Details object in the 
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
    for field in fields:
        if section.has_key(field):
            if "-" in field:
                d[field.replace("-", "")] = section[field]
            else:
                d[field] = section[field]
    return d


def find_package(name):
    """
    Queries the database for an existent package.
    If it does not exists, it creates a new package only with its name.
    
    :param name: the package name.
    
    :return: a `Package` object.
             
    :rtype: ``Package``
    
    .. versionadded:: 0.1
    """
    
    exists = Package.objects.filter(Package = name)
    if exists:
        return exists[0]
    else:
        p = Package(Package = name)
        p.save()
        return p

def create_relationship(fields):
    """
    Queries the database for an existent relation.
    If it does not exists, it creates a new relation.
                 
    :param fields: is a dictionary which contains the relation data. Its structure is similar to::  
                                  
                        {"related_package": "0ad-data", "relation_type": "depends",
                        "relation": ">=", "version": "0~r11863", "alt_id": None}
                   .
                   
    :return: a `Relation` object.
             
    :rtype: ``Relation``
    
    .. versionadded:: 0.1
    """

    exists = Relation.objects.filter(**fields)
    if exists:
        return exists[0]
    else:
        obj = Relation(**fields)
        obj.save()
        return obj


def create_tag(val):
    """
    Queries the database for an existent tag.
    If it does not exists, it creates a new tag.
    
    :param val: string with the value of the tag.
    
    :return: a `Tag` object.
             
    :rtype: ``Tag``
    
    .. versionadded:: 0.1
    """
    
    exists = Tag.objects.filter(Value = val)
    if exists:
        return exists[0]
    else:
        tag = Tag(Value = val)
        tag.save()
        return tag


def create_label(label_name, tag):
    """
    Queries the database for an existent label.
    If it does not exists, it creates a new label.
    
    :param label_name: a string with the name of the label.
    
    :param tag: a `Tag` object.
    
    :return: a `Label` object.
             
    :rtype: ``Label``
    
    .. versionadded:: 0.1
    """
    
    exists = Label.objects.filter(Name = label_name, Tags = tag)
    if exists:
        return exists[0]
    else:
        label = Label(Name = label_name, Tags = tag)
        label.save()
        return label


def record_package(section):
    """
    Queries the database for an existent package.
    If the package does exists but it doesn't have
    a maintainer, then the package data will be 
    updated acording to the fields of the section provided.
    If the package doesn't exists then it's created.
    
    :param section: paragraph which contains the package data.
    
    :return: a `Package` object.
             
    :rtype: ``Package``
    
    .. versionadded:: 0.1
    """
    
    exists = Package.objects.filter(Package = section['Package'])
    if exists:
        if not exists[0].Maintainer:
            exists.update(**select_paragraph_fields(section, package_fields))
            p = Package.objects.filter(Package = section['Package'])[0]
            p.Maintainer = record_maintainer(section['Maintainer'])
            p.save()
            return p
        else:
            return exists[0]
    else:
        fields = select_paragraph_fields(section, package_fields)
        m = record_maintainer(section['Maintainer'])
        p = Package(**fields)
        p.Maintainer = m
        p.save()
        record_tags(section, p)
        return p


def record_details(section, pq, dist):
    """
    Queries the database for the details of a given package.
    If there are no details then they are recorded.
    
    :param section: paragraph which contains the package data.
    
    :param pq: a `Package` object to which the details are related.
    
    :param dist: codename of the Canaima's version that will be recorded.
    
    :return: a `Details` object.
             
    :rtype: ``Details``
    
    .. versionadded:: 0.1
    """
    
    exists = Details.objects.filter(package = pq,
                                    Architecture = section['Architecture'],
                                    Distribution = dist)
    if exists:
        return exists[0]
    else:
        fields = select_paragraph_fields(section, detail_fields)
        d = Details(**fields)
        d.Distribution = dist
        d.save()
        pq.Details.add(d)
        return d


def record_tags(section, pq):
    """
    Processes the contents of the 'Tag' field in the provided paragraph,
    records the labels into the database and relates them to a package. 
    
    :param section: a paragraph which contains the package data.
    
    :param pq: a `Package` object to which the labels are related.
    
    .. versionadded:: 0.1
    """
    
    if section.has_key('Tag'):
        tag_list = section['Tag'].replace("\n", "").split(", ")
        for tag in tag_list:
            tag_parts = tag.split("::")
            value = create_tag(tag_parts[1])
            label = create_label(tag_parts[0], value)
            pq.Labels.add(label)


def record_relationship(dt, rtype, fields, alt_id = None):
    """
    Records a new relation in the database and then associates it to a `Details` object.
    
    :param dt: a `Details` object to which the relationship is related.
    
    :param rtype: a string indicating the relationship type.
    
    :param fields: a dictionary which contains the relation data. Its structure is similar to::
               
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
    
    if fields['version']:
        relation_version = fields['version'][0]
        number_version = fields['version'][1]
    else:
        relation_version = None
        number_version = None
    related = find_package(fields['name'])
    new_rel = create_relationship({"related_package": related,
                                   "relation_type": rtype,
                                   "relation" : relation_version,
                                   "version": number_version,
                                   "alt_id": alt_id})
    dt.Relations.add(new_rel)


def record_relations(details, relations_list):
    """
    Records a set of relations associated to a `Details` object.
    
    :param details: a `Details` object to which each relationship is related.
    
    :param relations_list: a list of tuples containing package relations to another pacakges.  
                      Its structure is similar to::
                      
                          [('depends', [[{'arch': None, 'name': u'libgl1-mesa-glx', 'version': None},
                          {'arch': None, 'name': u'libgl1', 'version': None}]],
                          [{'arch': None, 'name': u'0ad-data', 'version': (u'>=', u'0~r11863')}]), ('suggests', [])]

    .. versionadded:: 0.1
    """
    
    for relations in relations_list:
        alt_id = 1
        if relations[1]:
            for relation in relations[1]:
                if len(relation) > 1:
                    for relation_part in relation:
                        record_relationship(details, relations[0], relation_part, alt_id)
                    alt_id += 1
                else:
                    record_relationship(details, relations[0], relation[0])


def record_section(section, dist):
    """
    Records the content of a paragraph in the database.
    
    :param section: a paragraph which contains the package data.
    
    :param dist: codename of the Canaima's version that will be recorded.
    
    .. versionadded:: 0.1
    """
    
    #print "Registrando seccion -->", section['Package'], "-", section['Architecture']
    try:
        p = record_package(section)
        d = record_details(section, p, dist)
        record_relations(d, section.relations.items())
    except:
        print "Could not record %s" % section['Package']
        

def update_package(section):
    """
    Updates the basic data of a package in the database.
    
    :param section: a paragraph which contains the package data.
    
    :return: a `Package` object.
    
    :rtype: ``Package``
    
    .. versionadded:: 0.1
    """
    
    exists = Package.objects.filter(Package = section['Package'])
    exists.update(**select_paragraph_fields(section, package_fields))
    # Necesito encontrar una mejor forma de hacer esto: 
    # Actualizar los datos del paquete y mantener el objeto seleccionado 
    # para (en este caso) agregarle el mantenedor
    paquete = Package.objects.get(Package = section['Package'])
    if paquete.Maintainer.Name not in section['Maintainer'] or \
        paquete.Maintainer.Email not in section['Maintainer']: 
        paquete.Maintainer = record_maintainer(section['Maintainer'])
        paquete.save()
    return paquete


def update_details(pq, section, dist):
    """
    Updates the details of a Package in the database.
    
    :param pq: a `Package` object to which the details are related.
    
    :param section: a paragraph which contains the package data.
    
    :param dist: codename of the Canaima's version that will be updated.
    
    :return: a `Details` object.
             
    :rtype: ``Details``
    
    .. versionadded:: 0.1
    """
    
    exists = Details.objects.filter(package = pq,
                                    Architecture = section['Architecture'],
                                    Distribution = dist)
    exists.update(**select_paragraph_fields(section, detail_fields))
    d = Details.objects.filter(package = pq,
                               Architecture = section['Architecture'],
                               Distribution = dist)
    return d[0]


def update_section(section, dist):
    """
    Updates basic data and details of a package in the database.
    It also updates the package's relations.
    
    :param section: a paragraph which contains the package data.
    
    :param dist: codename of the Canaima's version that will be updated.
    
    .. versionadded:: 0.1
    """
    
    print "Actualizando la seccion -->", section['Package']
    p = update_package(section)
    d = update_details(p, section, dist)
    for r in d.Relations.all():
        d.Relations.remove(r)
        exists = Details.objects.filter(Relations = r)
        if not exists:
            r.delete()
    record_relations(d, section.relations.items())
    print "Actualizacion finalizada"


def update_package_list(file_path, dist):
    """
    Updates all packages from a debian control file.
    If a package exists but the MD5sum field is different from the one
    stored in the database then it updates the package data fields.
    If the package doesn't exists then its created.
    
    :param file_path: path to the debian control file.
    
    :param dist: codename of the Canaima's version that will be updated.
    
    .. versionadded:: 0.1
    """
    existent_packages = []
    actual_arch = None
    
    package_file = deb822.Packages.iter_paragraphs(file(file_path))
    print "Actualizando lista de paquetes"
    for section in package_file:
        existent_packages.append(section['Package'])
        if not actual_arch and section['Architecture'] != 'all':
            actual_arch = section['Architecture']
        exists = Details.objects.filter(package__Package = section['Package'], Architecture = section['Architecture'],
                                        Distribution = dist)
        if exists:
            if section['md5sum'] != exists[0].MD5sum:
                print "Se encontraron diferencias en la seccion -->", section['Package']
                print section['md5sum'], exists[0].MD5sum
                update_section(section, dist)
        else:
            record_section(section, dist)
            print "Se estan agregando nuevos detalles"
            
    # Selecciona los paquetes que coincidan con la arquitectura del packages actual            
    bd_packages = Package.objects.filter(Details__Distribution = dist).filter(Q(Details__Architecture = 'all') | 
                                                                              Q(Details__Architecture = actual_arch))
    for package in bd_packages:
        # En alguna parte debo eliminar relaciones o enlaces huerfanos
        
        # Si el paquete no esta en la lista, busca los detalles y borra aquellos obsoletos
        if package.Package not in existent_packages:
            for detail in package.Details.all():
                if detail.Distribution == dist and detail.Architecture == actual_arch:
                    print "Eliminando detalles de -->", package.Package
                    detail.delete()
            # Si el paquete no tiene mas detalles procede a eliminarlo
            if not package.Details.all():
                print "Eliminando -->", package.Package
                package.delete()
                

def update_dist_paragraphs(repository_root, dist):
    '''
    Updates a debian control file (Packages),
    comparing the the one in the repository with its local copy.
    If there are differences in the MD5sum field then the local
    copy is deleted and copied again from the repository.
    
    :param repository_root: url of the repository from which the Packages files will be updated.
    
    :param dist: codename of the Canaima's version that will be updated.
    
    .. versionadded:: 0.1
    '''
    
    source = os.path.join(repository_root, "dists", dist) 
    base = os.path.join(PACKAGECACHE, dist)
    
    try:
        datasource = urllib.urlopen(os.path.join(source, "Release"))
    except:
        datasource = None
    if datasource:
        rel = deb822.Release(datasource)
        for l in rel['MD5sum']:
            if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages$", l['name']):
                remote_file = os.path.join(source, l['name'])
                local_file = os.path.join(base,  l['name'])
                if not l['md5sum'] == md5Checksum(local_file):
                    os.remove(local_file)
                    urllib.urlretrieve(remote_file, local_file)
                    update_package_list(local_file, dist)
                else:
                    print "No hay cambios en -->", local_file
    else:
        print "No se ha podido llevar a cabo la actualizacion"


def update_package_cache():
    '''
    Scans the packagecache directory to get the existent 
    distributions and update them.
    It is assumed that the packagecache directory was created previously.
    '''
    
    if DEBUG:
        repository_root = LOCAL_ROOT
    else: 
        repository_root = CANAIMA_ROOT
    
    dists = scan_repository(repository_root)
    
    for dist in dists.keys():
        update_dist_paragraphs(repository_root, dist)
        
        
def create_cache_dirs(repository_root):
    '''
    Creates the packagecache and all other necessary directories to organize the
    debian control files (Packages) pulled from the repository.
    
    :param repository_root: url of the repository from which the Packages files will be pulled.
    
    .. versionadded:: 0.1
    '''
    
    local_dists =  scan_repository(repository_root)
    for dist in local_dists.items():
        try:
            datasource = urllib.urlopen(os.path.join(repository_root, dist[1]))
        except:
            datasource = None
        if datasource:
            rel = deb822.Release(datasource)
            if rel.has_key('MD5sum'):
                for l in rel['MD5sum']:
                    if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages$", l['name']):                        
                        comp = l['name'].split("/")
                        comp.pop()
                        partial_path = string.join(comp, "/")
                        
                        path_to_package_dir = os.path.join(PACKAGECACHE, dist[0], partial_path)
                        packages_file_path = os.path.join(PACKAGECACHE, dist[0], l['name']) 
                        remote_path = os.path.join(repository_root, "dists", dist[0], l['name'])
                        
                        if not find_dirs(path_to_package_dir):
                            os.makedirs(path_to_package_dir)
                        else:
                            os.remove(packages_file_path)
                        try:
                            urllib.urlretrieve(remote_path, packages_file_path)
                        except IOError:
                            print 'archivo %s no encontrado.' % (remote_path)
         
def fill_db_from_cache():
    '''
    Records the data from each Package file inside the packagecache folder into the database.
    
    .. versionadded:: 0.1
    '''
    
    local_dists = list_dirs(filter(None, PACKAGECACHE))
    for dist in local_dists:
        dist_sub_paths = filter(lambda p: "binary" in p, find_dirs(os.path.join(PACKAGECACHE, dist[0]))) 
        
        for path in dist_sub_paths:
            for p in find_files(path, "Packages"): 
                for section in deb822.Packages.iter_paragraphs(file(p)):
                    record_section(section, dist[0])
                    