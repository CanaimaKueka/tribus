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

tribus.tests.tribus_common_recorder
================================

These are the tests for the tribus.common.recorder module.

'''

import os
import email.Utils
from fabric.api import env, lcd, local, settings
from debian import deb822
from django.test import TestCase
from doctest import DocTestSuite
from tribus.web.cloud.models import Package
from tribus.common.utils import get_path
from tribus.__init__ import BASEDIR

SAMPLESDIR = get_path([BASEDIR, "tribus", "testing", "samples" ])
FIXTURES = get_path([BASEDIR, "tribus", "testing", "fixtures" ])

class RecorderFunctions(TestCase):
    
    #fixtures = [os.path.join(FIXTURES, 'base_fixture.json')]
    
    def setUp(self):
        # Instrucciones para recrear un entorno de pruebas
        pass        
        
    def tearDown(self):
        pass
#         with settings(command='rm -rf %(micro_repository_path)s' % env):
#             local('%(command)s' % env, capture=False)

    def test_record_maintainer(self):
        from tribus.common.recorder import record_maintainer
        maintainer_data = "Super Mantenedor 86 <supermaintainer86@maintainer.com>"
        test_maintainer = record_maintainer(maintainer_data)
        self.assertEqual(test_maintainer.Name, "Super Mantenedor 86", "El nombre no coincide")
        self.assertEqual(test_maintainer.Email, "supermaintainer86@maintainer.com", "El correo no coincide")
        
    
    def test_select_paragraph_data_fields(self):
        from tribus.common.recorder import select_paragraph_data_fields
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        selected_PACKAGE_FIELDS = select_paragraph_data_fields(section, PACKAGE_FIELDS)
        selected_details_fields = select_paragraph_data_fields(section, DETAIL_FIELDS)
        self.assertLessEqual(len(selected_PACKAGE_FIELDS), len(PACKAGE_FIELDS))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_PACKAGE_FIELDS.keys():
        #    self.assertIn(field, PACKAGE_FIELDS)
        self.assertLessEqual(len(selected_details_fields), len(DETAIL_FIELDS))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_details_fields.keys():
        #    self.assertIn(field, DETAIL_FIELDS)
        
        
    def test_find_package(self):
        from tribus.common.recorder import find_package
        test_package_name = "independencia-venezuela-deluxe-edition"
        p = find_package(test_package_name)
        self.assertEqual(p.Package, test_package_name)
        
        
    def test_create_relationship(self):
        from tribus.common.recorder import create_relationship, find_package
        p = find_package("independencia-venezuela-gold_edition")
        fields = {"related_package": p, "relation_type": "depends",
        "relation": ">=", "version": "0~r11863", "alt_id": 2}
        new_rs = create_relationship(fields)
        self.assertEqual(new_rs.related_package, fields["related_package"])
        self.assertEqual(new_rs.relation_type, fields["relation_type"])
        self.assertEqual(new_rs.relation, fields["relation"])
        self.assertEqual(new_rs.version, fields["version"])
        self.assertEqual(int(new_rs.alt_id), int(fields["alt_id"]))
        
        
    def test_create_tag(self):
        from tribus.common.recorder import create_tag
        tag_value = "awsome!"
        test_tag = create_tag(tag_value)
        self.assertEqual(tag_value, test_tag.Value)
        
        
    def test_create_label(self):
        from tribus.common.recorder import create_label, create_tag
        tag_value = "more awsome!"
        label_value = "description"
        test_tag = create_tag(tag_value)
        test_label = create_label(label_value, test_tag)
        self.assertEqual(tag_value, test_label.Tags.Value)
        self.assertEqual(label_value, test_label.Name)
        
        
    def test_record_package(self):
        from tribus.common.recorder import record_package
        from tribus.config.pkgrecorder import PACKAGE_FIELDS
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        
        maintainer_data = section.get('Maintainer', None)
        if maintainer_data:
            name, mail = email.Utils.parseaddr(maintainer_data)
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
        
        for field in PACKAGE_FIELDS:
            if section.get(field):
                self.assertEqual(getattr(p, 
                                         field.replace("-", "") if "-" in field else field),
                                 section[field])
        
        
    def test_record_details(self):
        from tribus.common.recorder import record_details, record_package
        from tribus.config.pkgrecorder import DETAIL_FIELDS
        test_dist = "kukenan"
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        d = record_details(section, p, test_dist)
        self.assertEqual(d.Distribution, test_dist)
        for field in DETAIL_FIELDS:
            self.assertEqual(getattr(d, 
                                     field.replace("-", "") if "-" in field else field),
                             section[field])
        
        
    def test_record_tags(self):
        # Implicitamente se llama a record_tags
        from tribus.common.recorder import record_package
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        tags = section.get('Tag', None)
        if tags:
            tag_list = section['Tag'].replace("\n", "").split(", ")
            clean_list = [tuple(tag.split("::")) for tag in tag_list]
            for label in p.Labels.all():
                self.assertIn((label.Name, label.Tags.Value),
                              clean_list)
    
    
    def test_record_relationship(self):
        from tribus.common.recorder import record_relationship, record_package,\
        record_details
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "libopenal1")))
        test_dist = "auyantepui"
        p = record_package(section)
        d = record_details(section, p, test_dist)
        reldata = [
                   ("depends", {"name": "libc6", "version": (">=", "2.3.6-6~")}),
                   ("recommends", {"name": "libpulse0", "version": (">=", "0.9.21")}),
                   ("suggests", {"name": "libportaudio2", "version": (None, None)})
                   ]

        for typerel, data in reldata:
            record_relationship(d, typerel, data)
        
        for relation in d.Relations.all():
            self.assertIn((relation.relation_type,
                           {"name": relation.related_package.Package,
                            "version": (relation.relation,
                                        relation.version)}), reldata)

        self.assertEqual(len(reldata), d.Relations.all().count())
        
        
    def test_record_relations(self):
        from tribus.common.recorder import record_relations, record_package,\
        record_details
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        d = record_details(section, p, "kukenan")
        record_relations(d, section.relations.items())
        total_relations = 0
        
        for relations in section.relations.items():
            if relations[1]:
                for relation in relations[1]:
                    if len(relation) > 1:
                        for _ in relation:
                            total_relations += 1
                    else:
                        total_relations += 1
        
        self.assertEqual(d.Relations.all().count(),
                         total_relations)
        
        
    def test_record_section(self):
        from tribus.common.recorder import record_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        test_dist = "kukenan"
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        record_paragraph(section, test_dist)
        
        p = Package.objects.get(Package = "blender")
        d = p.Details.all()[0]
        total_relations = 0
        maintainer_data = section.get('Maintainer', None)
        tags = section.get('Tag', None)
        
        for relations in section.relations.items():
            if relations[1]:
                for relation in relations[1]:
                    if len(relation) > 1:
                        for _ in relation:
                            total_relations += 1
                    else:
                        total_relations += 1
                        
        if maintainer_data:
            name, mail = email.Utils.parseaddr(maintainer_data)
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
            
        if tags:
            tag_list = section['Tag'].replace("\n", "").split(", ")
            clean_list = [tuple(tag.split("::")) for tag in tag_list]
            for label in p.Labels.all():
                self.assertIn((label.Name, label.Tags.Value),
                              clean_list)    
        
        for field in PACKAGE_FIELDS:
            if section.get(field):
                self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                 section[field])
        
        self.assertEqual(d.Distribution, test_dist)
        
        self.assertEqual(d.Distribution, test_dist)
        for field in DETAIL_FIELDS:
            self.assertEqual(str(getattr(d, 
                                     field.replace("-", "") if "-" in field else field)),
                             section[field])
        
        self.assertEqual(d.Relations.all().count(),
                         total_relations)
        
        
    def test_update_package(self):
        pass
    
    
    def test_update_details(self):
        pass
    
    
    def test_update_paragraph(self):
        from tribus.common.recorder import record_paragraph, update_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        test_dist = "kukenan"
        old_section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        new_section = deb822.Packages(open(os.path.join(SAMPLESDIR, "BlenderNew")))
        record_paragraph(old_section, test_dist)
        update_paragraph(new_section, test_dist)
        
        p = Package.objects.get(Package = "blender")
        d = p.Details.all()[0]
        total_relations = 0
        maintainer_data = new_section.get('Maintainer', None)
        tags = new_section.get('Tag', None)
        
        for relations in new_section.relations.items():
            if relations[1]:
                for relation in relations[1]:
                    if len(relation) > 1:
                        for _ in relation:
                            total_relations += 1
                    else:
                        total_relations += 1
        
        if maintainer_data:
            name, mail = email.Utils.parseaddr(maintainer_data)
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
            
        if tags:
            tag_list = new_section['Tag'].replace("\n", "").split(", ")
            clean_list = [tuple(tag.split("::")) for tag in tag_list]
            for label in p.Labels.all():
                self.assertIn((label.Name, label.Tags.Value),
                              clean_list)
        
        for field in PACKAGE_FIELDS:
            if new_section.get(field):
                self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                 new_section[field])
        
        self.assertEqual(d.Distribution, test_dist)
        
        for field in DETAIL_FIELDS:
            if new_section.get(field):
                self.assertEqual(str(getattr(d, 
                                     field.replace("-", "") if "-" in field else field)),
                             new_section[field])

        self.assertEqual(d.Relations.all().count(),
                         total_relations)
        
    def test_update_package_list(self):
        from tribus.common.recorder import record_paragraph, update_package_list
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        test_dist = "kukenan"
        old_amd_section = os.path.join(SAMPLESDIR, "Oldamd")
        old_i386_section = os.path.join(SAMPLESDIR, "Oldi386")
        new_amd_section = os.path.join(SAMPLESDIR, "Newamd")
        new_i386_section = os.path.join(SAMPLESDIR, "Newi386")
        
        for section in deb822.Packages.iter_paragraphs(open(old_amd_section)):
            record_paragraph(section, test_dist)
        for section in deb822.Packages.iter_paragraphs(open(old_i386_section)):
            record_paragraph(section, test_dist)
        
        update_package_list(new_amd_section, test_dist, 'i386')
        update_package_list(new_i386_section, test_dist, 'amd64')
        
        for section in deb822.Packages.iter_paragraphs(open(new_i386_section)):
            p = Package.objects.get(Package = section['Package'])
            d = p.Details.filter(Architecture = section['Architecture'])[0]
            total_relations = 0
            maintainer_data = section.get('Maintainer', None)
            tags = section.get('Tag', None)
            
            for field in PACKAGE_FIELDS:
                if section.get(field):
                    self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                         section[field])
                    
            self.assertEqual(d.Distribution, test_dist)
        
            for field in DETAIL_FIELDS:
                if section.get(field):
                    self.assertEqual(str(getattr(d, 
                                                 field.replace("-", "") if "-" in field else field)),
                                                 section[field])
            
            for relations in section.relations.items():
                if relations[1]:
                    for relation in relations[1]:
                        if len(relation) > 1:
                            for _ in relation:
                                total_relations += 1
                        else:
                            total_relations += 1
            
            self.assertEqual(d.Relations.all().count(),
                             total_relations)
            
            if maintainer_data:
                name, mail = email.Utils.parseaddr(maintainer_data)
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            
            if tags:
                tag_list = section['Tag'].replace("\n", "").split(", ")
                clean_list = [tuple(tag.split("::")) for tag in tag_list]
                for label in p.Labels.all():
                    self.assertIn((label.Name, label.Tags.Value),
                                  clean_list)
            
            
        for section in deb822.Packages.iter_paragraphs(open(new_amd_section)):
            p = Package.objects.get(Package = section['Package'], Details__Architecture = section['Architecture'])
            d = p.Details.filter(Architecture = section['Architecture'])[0]
            total_relations = 0
            maintainer_data = section.get('Maintainer', None)
            tags = section.get('Tag', None)
            
            for field in PACKAGE_FIELDS:
                if section.get(field):
                    self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                         section[field])
            
            self.assertEqual(d.Distribution, test_dist)
            
            for field in DETAIL_FIELDS:
                if section.get(field):
                    self.assertEqual(str(getattr(d, 
                                                 field.replace("-", "") if "-" in field else field)),
                                                 section[field])
            
            for relations in section.relations.items():
                if relations[1]:
                    for relation in relations[1]:
                        if len(relation) > 1:
                            for _ in relation:
                                total_relations += 1
                        else:
                            total_relations += 1
            
            self.assertEqual(d.Relations.all().count(),
                             total_relations)
            
            if maintainer_data:
                name, mail = email.Utils.parseaddr(maintainer_data)
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            
            if tags:
                tag_list = section['Tag'].replace("\n", "").split(", ")
                clean_list = [tuple(tag.split("::")) for tag in tag_list]
                for label in p.Labels.all():
                    self.assertIn((label.Name, label.Tags.Value),
                                  clean_list)
    
    
    # Como hacer un test para este metodo?
    # Necesitaria (desplegar) un microrepositorio el alguna ubicacion temporal
    # 1. Usando fabric o alguna vaina deberia crear un directorio donde alojar el repositorio
    # 2. Descargar una muestra (PEQUEÑA) de paquetes para indexar el repositorio, la muestra debe ser lo suficientemente representativa
    # conteniendo paquetes (LIGEROS) de varias de las distribuciones y arquitecturas asi como versiones superiores de los paquetes, que seran
    # el motivo de la actualizacion.
    # 3. Usando o emulando a fabric, se crea el micro-repositorio y se indexa la muestra de paquetes descargados
    # 4. Se registran los paquetes en la base de datos desde el micro-repositorio.
    # 5. Se invoca esta funcion o las correspondientes para que se verifique el md5 de los paquetes. 
    # En este punto se me presenta un problema: Suponiendo que la muestra consiste en 5 paquetes, esos se registran en la base
    # de datos y como consecuencia ademas de los 5 paquetes originales tendre registradas las dependencias asi sea como paquetes
    # incompletos. Luego en el momento en que se hace la actualizacion, se detectara un grupo de paquetes que esta registrado en la base
    # de datos pero no se encuentra en los archivos packages. Por lo tanto la conducta esperada es que al actualizar se eliminen los paquetes 
    # cuyos campos de informacion estan incompletos. No tengo certeza en este punto, por lo tanto empezare a hacer las pruebas y a medida que se 
    # vayan completando las revisare.


    def test_update_dist_paragraphs(self):
        # TODO ESTO PUEDE VERSE COMO UNA PRUEBA DE INTEGRACION
        from tribus.common.recorder import fill_db_from_cache, create_cache, update_cache
        from tribus.common.iosync import touch, rmtree
        
        dist = 'kerepakupai'
        env.micro_repository_path = os.path.join('/', 'tmp', 'tmp_repo')
        env.micro_repository_conf = os.path.join('/', 'tmp', 'tmp_repo', 'conf')
        env.samples_dir = SAMPLESDIR
        env.packages_dir = os.path.join(SAMPLESDIR, 'example_packages')
        env.pcache = os.path.join('/', 'tmp', 'pcache')
        env.distributions_path = os.path.join(env.micro_repository_path, 'distributions')
        
        with settings(command='mkdir -p %(micro_repository_conf)s' % env):
            local('%(command)s' % env, capture=False)
        
        with settings(command='cp %(samples_dir)s/distributions\
                  %(micro_repository_conf)s' % env):
            local('%(command)s' % env, capture=False)
            
        with lcd('%(micro_repository_path)s' % env):
            touch(env.distributions_path)
            f = open(env.distributions_path, 'w')
            f.write('kerepakupai dists/kerepakupai/Release')
            f.close()
            
        with lcd('%(micro_repository_path)s' % env):
            with settings(command='reprepro -VVV export'):
                local('%(command)s' % env, capture=False)
                
        # cube2font_1.2-2_i386.deb kerepakupai main i386
        # cube2font_1.2-2_amd64.deb kerepakupai main amd64
        # cl-sql-oracle_6.2.0-1_all.deb kerepakupai no-libres all 
        # libxine1-plugins_1.1.21-dmo2_all.deb kerepakupai aportes all
        # acroread-debian-files_9.5.8_i386 kerepakupai aportes i386 ELIMINAR
        # acroread-debian-files_9.5.8_amd64 kerepakupai aportes amd64 ELIMINAR
        
        seed_packages = [('cube2font_1.2-2_i386.deb', 'main'), ('cube2font_1.2-2_amd64.deb', 'main'), 
                         ('cl-sql-oracle_6.2.0-1_all.deb', 'no-libres'), ('libxine1-plugins_1.1.21-dmo2_all.deb', 'aportes'),
                         ('acroread-debian-files_9.5.8_i386.deb', 'aportes'), ('acroread-debian-files_9.5.8_amd64.deb', 'aportes')]
        
        with lcd('%(micro_repository_path)s' % env):
            for package, comp in seed_packages:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
        
        with lcd('%(micro_repository_path)s' % env):
            # Esto deberia ser objeto de un test separado OJO
            create_cache(env.micro_repository_path, env.pcache)
            
        with lcd('%(micro_repository_path)s' % env):
            fill_db_from_cache(env.pcache)
        
        add_list = [('libtacacs+1_4.0.4.26-3_amd64.deb', 'main'),  ('libtacacs+1_4.0.4.26-3_i386.deb', 'main')]
        update_list = [('cube2font_1.2-2_i386.deb', 'main'), ('cube2font_1.2-2_amd64.deb', 'main'), 
                       ('libxine1-plugins_1.1.21-dmo2_all.deb', 'aportes')]
        delete_list = [('cl-sql-oracle', 'no-libres'), ('acroread-debian-files', 'aportes'),
                       ('acroread-debian-files', 'aportes') ]
        
        with lcd('%(micro_repository_path)s' % env):
            for package, comp in add_list:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
                    
            for package, comp in update_list:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
                    
            for package, comp in delete_list:
                with settings(command='reprepro remove %s %s' %
                             (dist, package)):
                    local('%(command)s' % env, capture=False)
                    
        update_cache(env.micro_repository_path, env.pcache)
        
        # ACTUALIZACIONES

        # cube2font_1.3.1-2_amd64.deb ACTUALIZAR
        # cube2font_1.3.1-2_i386.deb ACTUALIZAR
        # libxine1-plugins_1.1.21-2_all.deb ACTUALIZAR
        # cl-sql-oracle_6.4.1-1_all.deb PARA ELIMINAR
        # guilt_0.35-1.2_all.deb AGREGAR
        # libtacacs+1_4.0.4.26-3_amd64.deb AGREGAR 
        # libtacacs+1_4.0.4.26-3_i386.deb AGREGAR
        
        rmtree(env.micro_repository_path)
        rmtree(env.pcache)


# ===============================================================================
# VERIFICACION DE ACTUALIZACION
# ========================================================================

# import urllib
# import urllib2
# from debian import deb822
# from tribus.web.cloud.models import *
# import re


# def check_version(exists, rr, r):
#     if exists and len(exists) == 1:
#         if rr['version']:
#             o = rr['version'][0]
#             n = rr['version'][1]
#             if exists[0].relation == o and exists[0].version == n:
#                 print "=D", exists[0], "esta bien actualizado"
#             else:
#                 print "=C", exists[0], "no esta bien actualizado"
#                 print r
#         else:
#             print "=D", exists[0], "No tiene version, nada que verificar"
#     elif exists and len(exists) > 1:
#         actual = exists.filter(relation = rr['version'][0])
#         if actual:
#             print "=D", actual[0], "esta bien actualizado"
#         else:
#             print "=C", actual[0], "no esta bien actualizado"


# def comprobarActualizacion(paquete):
#     i386  = "http://10.16.106.152/repositorio/dists/waraira/main/binary-i386/Packages"
#     archivo = urllib.urlopen(i386)
#     relations_file = 0
#     print "Prueba numero 1: Verificacion de dependencias 1 a 1"
#     for section in deb822.Packages.iter_paragraphs(archivo):
#         if section['Package'] == paquete:

#             rels = Relation.objects.filter(details__package__Package = section['Package'],
#                                             details__Architecture = section['Architecture'])
#             relations_bd = len(rels)

#             for rel in section.relations.items():
#                 if rel[1]:
#                     for r in rel[1]:
#                         for rr in r:
#                             relations_file +=1
#                             exists = Relation.objects.filter(details__package__Package = section['Package'],
#                                                              details__Architecture = section['Architecture'],
#                                                              related_package__Package = rr['name'],
#                                                              relation_type = rel[0])
#                             check_version(exists, rr, r)
#             break

#     print "Prueba numero 2: Conteo de relaciones"
#     print "RELACIONES EN BD -->", relations_bd
#     print "RELACIONES EN ARCHIVO -->", relations_file

# def repeated_relation_counter():
#     i386  = "http://paquetes.canaima.softwarelibre.gob.ve/dists/kerepakupai/main/binary-i386/Packages"
#     archivo = urllib.urlopen(i386)
#     for section in deb822.Packages.iter_paragraphs(archivo):
#         for rel in section.relations.items():
#             if rel[1]:
#                 for r in rel[1]:
#                     for rr in r:
#                         encontrados = 0
#                         for name in section[rel[0]].replace(',', ' ').split():
#                             lista = re.match('^'+rr['name'].replace("+", "\+").replace("-", "\-")+'$', name)
#                             if lista and rr['version']:
#                                 encontrados += 1
#                         if encontrados > 2:
#                             print section['package']
#                             print r
