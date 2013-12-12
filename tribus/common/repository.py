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
======================

This module contains common functions to manage local and remote repositories.

'''

import urllib, re, os, sys, string, random, gzip, urllib2
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from tribus.config.pkgrecorder import LOCAL_ROOT, CANAIMA_ROOT, SAMPLES_LISTS, SAMPLES_PACKAGES, SAMPLES
from tribus.common.utils import list_files, scan_repository


def init_sample_packages():
    os.makedirs(SAMPLES_LISTS)
    dist_releases = scan_repository(CANAIMA_ROOT)
    for release in dist_releases.items():
        try:
            datasource = urllib.urlopen(os.path.join(CANAIMA_ROOT, release[1]))
        except:
            datasource = None
        if datasource:
            rel = deb822.Release(datasource)
            if rel.has_key('MD5sum'):
                for l in rel['MD5sum']:
                    if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", l['name']):
                        print "Seleccionando paquetes en -->", l['name']
                        list_name = string.join( l['name'].split("/"), "_")
                        list_file = os.path.join(SAMPLES_LISTS, string.join([release[0], list_name], "_"))
                        package_url = os.path.join(CANAIMA_ROOT, "dists", release[0], l['name'])
                        select_sample_packages(package_url, list_file, False)
                        
def select_sample_packages(package_url, package_list, include_relations = False):
    inicial = {}
    relaciones = []
    final = {}
    archivo = open(package_list, 'w')
    tmp_path = os.path.join(SAMPLES, "tmpckg.gzip")
    urllib.urlretrieve(package_url, tmp_path)
    for section in deb822.Packages.iter_paragraphs(gzip.open(tmp_path)):
        rnd = random.randint(0, 500)
        if section.has_key('Installed-Size'):
            if rnd == 500 and int(section['Installed-Size']) < 500:
                inicial[section['Package']] = section['Filename']
                archivo.write(section['filename']+"\n")
                for relations in section.relations.items():
                    if relations[1]:
                        for relation in relations[1]:
                            for r in relation:
                                relaciones.append(r['name'])
    
    if include_relations:
        remote_packages = urllib.urlopen(package_url)
                   
        for section in deb822.Packages.iter_paragraphs(remote_packages):
            if section['Package'] in relaciones and int(section['Installed-Size']) < 500:
                final[section['Package']] = section['Filename']
                archivo.write(section['filename']+"\n")
    
    archivo.close()
    print "Paquetes seleccionados -->", len(inicial)
    
def download_sample_packages():
    files_list = list_files(SAMPLES_LISTS)
    for f in files_list:
        pre_dist_path = f.split("/")[-1]
        dist_path = pre_dist_path.split("_")
        dist_path.pop()
        final_path = string.join(dist_path, "/")
        download_package_list(f, os.path.join(SAMPLES_PACKAGES, final_path))   
    urllib.urlretrieve(os.path.join(CANAIMA_ROOT, "distributions"), os.path.join(LOCAL_ROOT, "distributions"))
    
def download_package_list(file_with_package_list, download_dir):
    os.makedirs(download_dir)
    archivo = open(file_with_package_list, 'r')
    remote_root = "http://paquetes.canaima.softwarelibre.gob.ve"
    linea = archivo.readline().strip("\n")
    
    while linea:
        l = linea.split("/")
        print "Descargando ---->", l[-1]
        urllib.urlretrieve(os.path.join(remote_root, linea), os.path.join(download_dir, l[-1]))
        linea = archivo.readline().strip("\n")
        
    archivo.close()
