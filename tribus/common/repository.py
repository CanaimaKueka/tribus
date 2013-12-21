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

import urllib, re, os, sys, random, gzip
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from tribus.config.pkgrecorder import LOCAL_ROOT, CANAIMA_ROOT, SAMPLES
from tribus.common.utils import scan_repository, find_files

def select_sample_packages(package_url, package_list, include_relations = False):
    inicial = {}
    relaciones = []
    final = {}
    archivo = open(package_list, 'w')
    # Esto deberia ser una constante declarada en otra parte
    tmp_path = os.path.join(SAMPLES, "tmp.gzip")
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
    print "%s Paquetes seleccionados de %s "% (len(inicial), package_url)


def init_sample_packages():
    # Si la ruta para alojar los paquetes no existe se crea
    if not os.path.isdir(SAMPLES):
        os.makedirs(SAMPLES)
    # Extraigo las distribuciones desde el repositorio oficial
    dist_releases = scan_repository(CANAIMA_ROOT)
    
    for release in dist_releases.items():
        try:
            # Se trata de un archivo remoto, por lo tanto lo abro a traves de la url
            datasource = urllib.urlopen(os.path.join(CANAIMA_ROOT, "dists", release[0], "Release"))
        except:
            print "Se produjo un error leyendo los Release"
            datasource = None
            
        if datasource:
            rel = deb822.Release(datasource)
            #if rel.has_key('MD5sum'):
            if 'MD5sum' in rel:
                for l in rel['MD5sum']:
                    # Para hacer el proceso mas rapido se descargan los Packages comprimidos
                    if re.match("[\w]*-?[\w]*/[\w]*-[\w]*/Packages.gz$", l['name']):
                        component, architecture, _ = l['name'].split("/")
                        list_path = os.path.join(SAMPLES, release[0], component, architecture)
                        
                        if not os.path.isdir(list_path):
                            os.makedirs(list_path)
                        
                        f = os.path.join(list_path, "list")  
                        
                        if not os.path.isfile(f):
                            package_url = os.path.join(CANAIMA_ROOT, "dists", release[0], l['name'])
                            try:
                                select_sample_packages(package_url, f, False)
                            except:
                                print "Hubo un error descargando %s" % package_url

    if os.path.isfile(os.path.join(SAMPLES, "tmp.gzip")):
        os.remove(os.path.join(SAMPLES, "tmp.gzip"))
    
def download_sample_packages():
    files_list = find_files(SAMPLES, 'list')
    for f in files_list:
        download_path = os.path.dirname(f)
        download_package_list(f, download_path)   
    urllib.urlretrieve(os.path.join(CANAIMA_ROOT, "distributions"), os.path.join(LOCAL_ROOT, "distributions"))
    
def download_package_list(file_with_package_list, download_dir):
    archivo = open(file_with_package_list, 'r')
    linea = archivo.readline().strip("\n")
    while linea:
        l = linea.split("/")
        try:
            print "Descargando ---->", l[-1]
            urllib.urlretrieve(os.path.join(CANAIMA_ROOT, linea), os.path.join(download_dir, l[-1]))
        except:
            print "Hubo un error intentando descargar el paquete %s " % l[-1]
        linea = archivo.readline().strip("\n")
    archivo.close()

def main():
    init_sample_packages()
    download_sample_packages()
    
main()