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
from tribus.common.utils import find_files, readconfig

logger = get_logger()


def init_sample_packages(repository_root, samples_dir):
    '''
    Creates a directory structure to store packages for its later use
    in a test package repository.
    
    :param repository_root: url of the repository used.
    
    :param samples_dir: directory that will be used to store the examples for the repository.
    
    .. versionadded:: 0.1
    '''
    
    if not os.path.isdir(samples_dir):
        os.makedirs(samples_dir)
    
    # Puede que exista una forma mas sencilla de obtener los nombres
    dist_releases = (branch.split()
                     for branch in
                     readconfig(os.path.join(repository_root,
                                             "distributions")))
    for release, _ in dist_releases:
        release_path = os.path.join(repository_root, "dists", release, "Release")
        try:
            # Riesgo poco probable de que el Release no tenga MD5sum
            md5list = deb822.Release(urllib.urlopen(release_path)).get('MD5sum')
        except urllib2.URLError, e:
            logger.warning('Could not read release file in %s, error code #%s' % (release_path, e.code))
        else:
            for l in md5list:
                if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", l['name']):
                    list_dir = os.path.join(samples_dir, release,
                                            os.path.dirname(l['name']))
                    if not os.path.isdir(list_dir):
                        os.makedirs(list_dir)
                    list_path = os.path.join(list_dir, "list")
                    if not os.path.isfile(list_path):
                        control_f_path = os.path.join(repository_root, "dists",
                                                      release, l['name'])
                        select_sample_packages(control_f_path, list_path,
                                               samples_dir, False)
    if os.path.isfile(os.path.join(samples_dir, "tmp.gzip")):
        os.remove(os.path.join(samples_dir, "tmp.gzip"))


def select_sample_packages(remote_control_file_path, package_list_path,
                           samples_dir, include_relations=False):
    '''
    Reads a control file and makes a random selection of packages, 
    then downloads the selected ones.
    
    :param remote_control_file_path: path to the control file from which the packages will be selected.
    
    :param package_list_path: path to the file where the package name and location will be written.
    
    :param samples_dir: directory that will be used to store the examples for the repository.
    
    :param include_relations: si es True se descargaran tambien las relaciones de cada paquete seleccionado
    que cuyo tamano sea menor a 500 kilobytes. Si es Falso no se descargaran los paquetes relacionados.

    .. versionadded:: 0.1
    '''
    
    # No sabria decir que es lo que esta mal aqui
    # pero no me gusta mucho la forma como se hace esto
    tmp_file = os.path.join(samples_dir, "tmp.gzip")
    
    try:
        urllib.urlretrieve(remote_control_file_path, tmp_file)
    except urllib2.URLError, e:
        logger.warning('Could not get control file %s, error code #%s' % (remote_control_file_path, e.code))
    else:
        selected = 0
        # No hay manejo de excepciones en caso de fallas al intentar leer el archivo
        archivo = open(package_list_path, 'w')
        for section in deb822.Packages.iter_paragraphs(gzip.open(tmp_file)):
            # Debe existir un a mejor forma de seleccionar elementos aleatorios
            rnd = random.randint(0, 500)
            size = section.get('Installed-Size', None)
            if size:
                if rnd == 500 and int(size) < 500:
                    selected += 1
                    archivo.write(section['filename'] + "\n")
                    if include_relations:
                        relaciones = []
                        for _, relations in section.relations.items():
                            if relations:
                                for relation in relations:
                                    for r in relation:
                                        relaciones.append(r['name'])
        # El tener que volver a leer el archivo para obtener las
        # dependencias hace que el proceso sea mas lento
        if include_relations:
            for section in deb822.Packages.iter_paragraphs(gzip.open(tmp_file)):
                if section['Package'] in relaciones and int(section['Installed-Size']) < 500:
                    selected += 1
                    archivo.write(section['filename'] + "\n")
        archivo.close()
        logger.info("%s packages selected from %s " % (selected, remote_control_file_path))


def download_sample_packages(repository_root, samples_dir):
    '''
    Reads all the files named 'list' present in the samples directory
    and downloads the packages in each 'list' file.
    
    :param repository_root: url of the repository used.
    
    :param samples_dir: directory that will be used to store the examples for the repository.
    
    .. versionadded:: 0.1
    '''
    
    files_list = find_files(samples_dir, 'list')
    for f in files_list:
        download_path = os.path.dirname(f)
        with open(f) as list_file:
            # for line in list_file:
            for line in list_file.readlines():
                l = line.replace('\n', '').split('/')
                try:
                    if not os.path.isfile(os.path.join(download_path, l[-1])):
                        logger.info("Downloading -> %s" % l[-1])
                        urllib.urlretrieve(os.path.join(repository_root, line),
                                           os.path.join(download_path, l[-1]))
                except urllib2.URLError, e:
                    logger.warning('Could not get %s, error code #%s' % (l[-1], e.code))


def get_selected_packages(remote_root, samples_dir, list_path):
    '''
    Creates a directory structure to store package samples for its later use
    in a test package repository.
    
    :param samples_dir: directory that will be used to store the examples for the repository.
    
    .. versionadded:: 0.1
    '''
    
    samples = readconfig(list_path, None, False, False)
    for sample in samples:
        dist, comp, pool = sample.split()
        dest = os.path.join(samples_dir, dist, comp)
        
        if not os.path.isdir(dest):
            os.makedirs(dest)
        
        try:
            sample_name = os.path.basename(pool)
            if not os.path.isfile(os.path.join(dest, sample_name)):
                logger.info("Downloading -> %s" % sample_name)
                urllib.urlretrieve(os.path.join(remote_root, pool),
                                   os.path.join(dest, sample_name))
        except urllib2.URLError, e:
            logger.warning('Could not get %s, error code #%s' % (sample_name, e.code))