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

tribus.common.repository
========================

This module contains common functions to manage local and remote repositories.

'''

#=========================================================================
# TODO:
# 1. Hacer tests para estas funciones.
# 2. Revisar procedimientos, colocar nombres mas apropiados de acuerdo 
#    a las convenciones de nombres.
#=========================================================================

import re
import os
import gzip
import random
import urllib
import urllib2
from debian import deb822
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from tribus.common.logger import get_logger
from tribus.config.pkgrecorder import LOCAL_ROOT, CANAIMA_ROOT, SAMPLES
from tribus.common.utils import find_files, readconfig

logger = get_logger()

def select_sample_packages(remote_control_file_path, package_list_path,
                           include_relations=False):
    '''
    Reads a control file and makes a random selection of packages, 
    then downloads the selected ones.
    
    :param remote_control_file_path: path to the control file from which the packages will be selected.
    
    :param package_list_path: path to the file where the package name and location will be written.
    
    :param include_relations: si es True se descargaran tambien las relaciones de cada paquete seleccionado
    que cuyo tamano sea menor a 500 kilobytes. Si es Falso no se descargaran los paquetes relacionados.

    .. versionadded:: 0.1
    '''
    
    inicial = {}
    relaciones = []
    final = {}
    archivo = open(package_list_path, 'w')
    # Esto deberia ser una constante declarada en otra parte
    tmp_path = os.path.join(SAMPLES, "tmp.gzip")
    
    try:
        urllib.urlretrieve(remote_control_file_path, tmp_path)
    except urllib2.URLError, e:
        logger.warning('Could not read control file in %s, error code #%s' % (remote_control_file_path, e.code))
    else:
        for section in deb822.Packages.iter_paragraphs(gzip.open(tmp_path)):
            rnd = random.randint(0, 500)
            size = section.get('Installed-Size', None)
            if size:
                if rnd == 500 and int(size) < 500:
                    inicial[section['Package']] = section['Filename']
                    archivo.write(section['filename'] + "\n")
                    for relations in section.relations.items():
                        if relations[1]:
                            for relation in relations[1]:
                                for r in relation:
                                    relaciones.append(r['name'])
    
        if include_relations:
            remote_packages = urllib.urlopen(remote_control_file_path)
            for section in deb822.Packages.iter_paragraphs(remote_packages):
                if section['Package'] in relaciones and int(section['Installed-Size']) < 500:
                    final[section['Package']] = section['Filename']
                    archivo.write(section['filename'] + "\n")
    
        archivo.close()
        logger.info("%s packages selected from %s " % (len(inicial), remote_control_file_path))


def init_sample_packages():
    '''
    Creates a directory structure to store packages for its later use
    in a test package repository.
    
    .. versionadded:: 0.1
    '''
    
    if not os.path.isdir(SAMPLES):
        os.makedirs(SAMPLES)
        
    dist_releases = (branch.split()
                     for branch in readconfig(os.path.join(CANAIMA_ROOT,
                                                            "distributions")))

    for release, _ in dist_releases:
        release_path = os.path.join(CANAIMA_ROOT, "dists", release, "Release")
        try:
            datasource = urllib.urlopen(release_path)
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (release_path, e.code))
        else:
            rel = deb822.Release(datasource)
            md5list = rel.get('MD5sum', None)
            if md5list:
                for l in md5list:
                    if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", l['name']):
                        component, architecture, _ = l['name'].split("/")
                        list_path = os.path.join(
                            SAMPLES,
                            release,
                            component,
                            architecture)
                        if not os.path.isdir(list_path):
                            os.makedirs(list_path)
                        f = os.path.join(list_path, "list")
                        if not os.path.isfile(f):
                            package_url = os.path.join(
                                CANAIMA_ROOT,
                                "dists",
                                release,
                                l['name'])
                            select_sample_packages(package_url, f, False)
                            
    if os.path.isfile(os.path.join(SAMPLES, "tmp.gzip")):
        os.remove(os.path.join(SAMPLES, "tmp.gzip"))


def download_sample_packages():
    '''
    Reads all the files named 'list' present in the SAMPLES directory
    and downloads the packages in each 'list' file.
    
    .. versionadded:: 0.1
    '''
    
    files_list = find_files(SAMPLES, 'list')
    for f in files_list:
        download_path = os.path.dirname(f)
        archivo = open(f, 'r')
        linea = archivo.readline().strip("\n")
        while linea:
            l = linea.split("/")
            try:
                logger.info("Downloading ->", l[-1])
                urllib.urlretrieve(os.path.join(CANAIMA_ROOT, linea),
                                   os.path.join(download_path, l[-1]))
            except urllib2.URLError, e:
                logger.warning('Could not get %s, error code #%s' % (l[-1], e.code))
            linea = archivo.readline().strip("\n")
        archivo.close()
    # Esto deberia tener otro try
    urllib.urlretrieve(os.path.join(CANAIMA_ROOT, "distributions"),
                       os.path.join(LOCAL_ROOT, "distributions"))
