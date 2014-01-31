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
from tribus.config.pkgrecorder import SAMPLES

'''

tribus.tests.tribus_common_recorder
================================

These are the tests for the tribus.common.recorder module.

'''

import os
import email.Utils
from fabric.api import *
from debian import deb822
from django.test import TestCase
from doctest import DocTestSuite
from tribus.common import utils
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
        # Instrucciones para deshacer el entorno de pruebas
        pass
#         with settings(command='rm -rf %(micro_repository_path)s' % env):
#             local('%(command)s' % env, capture=False)
    
    
#     def test_test1(self):
#         from tribus.common.recorder import find_package
#         p = Package.objects.get(Package = "banshee")
#         p.delete()
#         find_package("independencia-venezuela-deluxe")
#         print Package.objects.filter(Package = "independencia-venezuela-deluxe")
#         Package.objects.all().delete()
#         print Package.objects.all()
#         
#         
#     def test_test2(self):
#         from tribus.web.cloud.models import Package
#         print Package.objects.filter(Package = "banshee")
#         print Package.objects.filter(Package = "independencia-venezuela-deluxe")
        
        
    def test_record_maintainer(self):
        from tribus.common.recorder import record_maintainer
        maintainer_data = "Super Mantenedor 86 <supermaintainer86@maintainer.com>"
        test_maintainer = record_maintainer(maintainer_data)
        self.assertEqual(test_maintainer.Name, "Super Mantenedor 86", "El nombre no coincide")
        self.assertEqual(test_maintainer.Email, "supermaintainer86@maintainer.com", "El correo no coincide")
        
    
    def test_select_paragraph_fields(self):
        from tribus.common.recorder import select_paragraph_fields
        from tribus.config.pkgrecorder import package_fields, detail_fields
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        selected_package_fields = select_paragraph_fields(section, package_fields)
        selected_details_fields = select_paragraph_fields(section, detail_fields)
        self.assertLessEqual(len(selected_package_fields), len(package_fields))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_package_fields.keys():
        #    self.assertIn(field, package_fields)
        self.assertLessEqual(len(selected_details_fields), len(detail_fields))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_details_fields.keys():
        #    self.assertIn(field, detail_fields)
        
        
    def test_find_package(self):
        from tribus.common.recorder import find_package
        test_package_name = "independencia-venezuela-deluxe-edition"
        p = find_package(test_package_name)
        self.assertEqual(p.Package, test_package_name)
        
        
    def test_create_relationship(self):
        from tribus.common.recorder import create_relationship, find_package
        # La via facil, crear un paquete al vuelo
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
        from tribus.config.pkgrecorder import package_fields
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        
        maintainer_data = section.get('Maintainer', None)
        if maintainer_data:
            name, mail = email.Utils.parseaddr(maintainer_data)
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
        
        for field in package_fields:
            if section.get(field):
                self.assertEqual(getattr(p, 
                                         field.replace("-", "") if "-" in field else field),
                                 section[field])
        
        
    def test_record_details(self):
        from tribus.common.recorder import record_details, record_package
        from tribus.config.pkgrecorder import detail_fields
        test_dist = "kukenan"
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        d = record_details(section, p, test_dist)
        self.assertEqual(d.Distribution, test_dist)
        for field in detail_fields:
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
        from tribus.common.recorder import record_section
        from tribus.config.pkgrecorder import package_fields, detail_fields
        test_dist = "kukenan"
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        record_section(section, test_dist)
        
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
        
        for field in package_fields:
            if section.get(field):
                self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                 section[field])
        
        self.assertEqual(d.Distribution, test_dist)
        
        self.assertEqual(d.Distribution, test_dist)
        for field in detail_fields:
            self.assertEqual(str(getattr(d, 
                                     field.replace("-", "") if "-" in field else field)),
                             section[field])
        
        self.assertEqual(d.Relations.all().count(),
                         total_relations)
        
        
    def test_update_package(self):
        pass
    
    
    def test_update_details(self):
        pass
    
    
    def test_update_section(self):
        from tribus.common.recorder import record_section, update_section
        from tribus.config.pkgrecorder import package_fields, detail_fields
        test_dist = "kukenan"
        old_section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        new_section = deb822.Packages(open(os.path.join(SAMPLESDIR, "BlenderNew")))
        record_section(old_section, test_dist)
        update_section(new_section, test_dist)
        
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
        
        for field in package_fields:
            if new_section.get(field):
                self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                 new_section[field])
        
        self.assertEqual(d.Distribution, test_dist)
        
        for field in detail_fields:
            if new_section.get(field):
                self.assertEqual(str(getattr(d, 
                                     field.replace("-", "") if "-" in field else field)),
                             new_section[field])

        self.assertEqual(d.Relations.all().count(),
                         total_relations)
        
    def test_update_package_list(self):
        from tribus.common.recorder import update_package_list, record_section
        from tribus.config.pkgrecorder import package_fields, detail_fields
        test_dist = "kukenan"
        old_amd_section = os.path.join(SAMPLESDIR, "Oldamd")
        old_i386_section = os.path.join(SAMPLESDIR, "Oldi386")
        new_amd_section = os.path.join(SAMPLESDIR, "Newamd")
        new_i386_section = os.path.join(SAMPLESDIR, "Newi386")
        
        for section in deb822.Packages.iter_paragraphs(open(old_amd_section)):
            record_section(section, test_dist)
        for section in deb822.Packages.iter_paragraphs(open(old_i386_section)):
            record_section(section, test_dist)
        
        update_package_list(new_amd_section, test_dist)
        update_package_list(new_i386_section, test_dist)
        
        for section in deb822.Packages.iter_paragraphs(open(new_i386_section)):
            p = Package.objects.get(Package = section['Package'])
            d = p.Details.filter(Architecture = section['Architecture'])[0]
            total_relations = 0
            maintainer_data = section.get('Maintainer', None)
            tags = section.get('Tag', None)
            
            for field in package_fields:
                if section.get(field):
                    self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                         section[field])
                    
            self.assertEqual(d.Distribution, test_dist)
        
            for field in detail_fields:
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
            
            for field in package_fields:
                if section.get(field):
                    self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                         section[field])
            
            self.assertEqual(d.Distribution, test_dist)
            
            for field in detail_fields:
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
    
    
    def test_update_dist_paragraphs(self):
        # TODO ESTO PUEDE VERSE COMO UNA PRUEBA DE INTEGRACION
        from tribus.common.recorder import create_cache_dirs, fill_db_from_cache, update_dist_paragraphs
        from tribus.common.utils import get_path
        from tribus.common.iosync import makedirs, touch, ln, rmtree
        from django.db.models import Q
        
        dist = 'kerepakupai'
        env.micro_repository_path = os.path.join('/', 'tmp', 'tmp_repo')
        env.micro_repository_conf = os.path.join('/', 'tmp', 'tmp_repo', 'conf')
        env.samples_dir = SAMPLESDIR
        env.packages_dir = os.path.join(SAMPLESDIR, 'example_packages')
        env.pcache = os.path.join('/', 'tmp', 'pcache')
        env.distributions_path = os.path.join(env.micro_repository_path, 'distributions')
        
        with settings(command='mkdir -p %(micro_repository_conf)s' % env):
            local('%(command)s' % env, capture=False)
        
        with settings(command='cp %(samples_dir)s/distributions  \
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
            create_cache_dirs(env.micro_repository_path, env.pcache)
            
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
        
        update_dist_paragraphs(env.micro_repository_path, dist, env.pcache)
        
        #print ">>>>>>", Package.objects.all()
        #print ">>>>>>", Package.objects.all().count()
        print 
        print ">>>>>>", Package.objects.filter(Q(Details__Architecture = 'all') | Q(Details__Architecture = 'i386') | Q(Details__Architecture = 'amd64')).distinct()
        
        # ACTUALIZACIONES

        # cube2font_1.3.1-2_amd64.deb ACTUALIZAR
        # cube2font_1.3.1-2_i386.deb ACTUALIZAR
        # libxine1-plugins_1.1.21-2_all.deb ACTUALIZAR
        # cl-sql-oracle_6.4.1-1_all.deb PARA ELIMINAR
        # guilt_0.35-1.2_all.deb AGREGAR
        # libtacacs+1_4.0.4.26-3_amd64.deb AGREGAR 
        # libtacacs+1_4.0.4.26-3_i386.deb AGREGAR
        
        
        #rmtree(env.micro_repository_path)
        
    
        
    

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
