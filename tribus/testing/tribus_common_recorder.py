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
import gzip
import email.Utils
from fabric.api import env, lcd, local, settings
from debian import deb822
from django.test import TestCase
from doctest import DocTestSuite
from tribus.__init__ import BASEDIR
from tribus.common.utils import get_path
from tribus.web.cloud.models import Package

SAMPLESDIR = get_path([BASEDIR, "tribus", "testing", "samples" ])
FIXTURES = get_path([BASEDIR, "tribus", "testing", "fixtures" ])

class RecorderFunctions(TestCase):
    #fixtures = [os.path.join(FIXTURES, 'base_fixture.json')]
    
    def setUp(self):
        pass        
        
    def tearDown(self):
        pass

    def test_record_maintainer(self):
        from tribus.common.recorder import record_maintainer
        maintainer_data = "Super Mantenedor 86 <supermaintainer86@maintainer.com>"
        test_maintainer = record_maintainer(maintainer_data)
        self.assertEqual(test_maintainer.Name, "Super Mantenedor 86", "El nombre no coincide")
        self.assertEqual(test_maintainer.Email, "supermaintainer86@maintainer.com", "El correo no coincide")
    
    
#     def test_record_maintainer_exception(self):
#         from tribus.common.recorder import record_maintainer
#         from django.db import DatabaseError
#         maintainer_data = "Simón José Antonio de la Santísima Trinidad Bolívar y Ponte Palacios y Blanco <simonjoséantoniodelasantísimatrinidadbolívarypontepalaciosyblanco@simonjoséantoniodelasantísimatrinidadbolívarypontepalaciosyblanco.com"
#         self.assertRaises(DatabaseError, record_maintainer, maintainer_data)
    
    
    def test_select_paragraph_data_fields(self):
        from tribus.common.recorder import select_paragraph_data_fields
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        selected_pckage_fields = select_paragraph_data_fields(section, PACKAGE_FIELDS)
        selected_details_fields = select_paragraph_data_fields(section, DETAIL_FIELDS)
        self.assertLessEqual(len(selected_pckage_fields), len(PACKAGE_FIELDS))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_PACKAGE_FIELDS.keys():
        #    self.assertIn(field, PACKAGE_FIELDS)
        self.assertLessEqual(len(selected_details_fields), len(DETAIL_FIELDS))
        # La prueba falla si se verifican los campos en cuyo nombre hay un guion (-)
        # hace falta una solucion
        #for field in selected_details_fields.keys():
        #    self.assertIn(field, DETAIL_FIELDS)


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
        from tribus.common.recorder import record_package
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        tags = section.get('Tag', None)
        if tags:
            tag_list = section['Tag'].replace("\n", "").split(", ")
            clean_list = [tuple(tag.split("::")) for tag in tag_list]
            for label in p.Labels.all():
                self.assertIn((label.Name, label.Tags.Value), clean_list)
    
    
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
        from tribus.web.cloud.models import Relation
        section = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        p = record_package(section)
        d = record_details(section, p, "kukenan")
        record_relations(d, section.relations.items())
        total_relations = 0
        
        for relation_type, relations in section.relations.items():
            if relations:
                for relation in relations:
                    if len(relation) > 1:
                        for element in relation:
                            version = element.get('version', None)
                            if version:
                                vn, vo = version
                            else:
                                vn, vo = (None, None)
                            self.assertTrue(Relation.objects.get(relation_type = relation_type,
                                               related_package__Package = element['name'],
                                               version = vo, relation = vn))
                            total_relations += 1
                    else:
                        version = relation[0].get('version', None)
                        if version:
                            vn, vo = version
                        else:
                            vn, vo = (None, None)
                        self.assertTrue(Relation.objects.get(relation_type = relation_type,
                                               related_package__Package = relation[0]['name'],
                                               version = vo, relation = vn))
                        total_relations += 1
        self.assertEqual(d.Relations.all().count(), total_relations)
        
        
    def test_record_paragraph(self):
        from tribus.common.recorder import record_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        test_dist = "kukenan"
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        record_paragraph(paragraph, test_dist)
        p = Package.objects.get(Package = "blender")
        d = p.Details.all()[0]
        total_relations = 0
        maintainer_data = paragraph.get('Maintainer', None)
        tags = paragraph.get('Tag', None)
        
        for relations in paragraph.relations.items():
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
            tag_list = paragraph['Tag'].replace("\n", "").split(", ")
            clean_list = [tuple(tag.split("::")) for tag in tag_list]
            for label in p.Labels.all():
                self.assertIn((label.Name, label.Tags.Value),
                              clean_list)    
        
        for field in PACKAGE_FIELDS:
            if paragraph.get(field):
                self.assertEqual(str(getattr(p,
                                         field.replace("-", "") if "-" in field else field)),
                                 paragraph[field])
        
        self.assertEqual(d.Distribution, test_dist)
        
        self.assertEqual(d.Distribution, test_dist)
        for field in DETAIL_FIELDS:
            self.assertEqual(str(getattr(d, 
                                     field.replace("-", "") if "-" in field else field)),
                             paragraph[field])
        
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


    def test_create_cache(self):
        pass
    
    
#     REEVALUAR ESTE TEST!!!! 
#     def test_update_cache(self):
#         # TODO ESTO PUEDE VERSE COMO UNA PRUEBA DE INTEGRACION
#         from tribus.common.recorder import fill_db_from_cache, create_cache, update_cache
#         from tribus.common.iosync import touch, rmtree
#         
#         dist = 'kerepakupai'
#         env.micro_repository_path = os.path.join('/', 'tmp', 'tmp_repo')
#         env.micro_repository_conf = os.path.join('/', 'tmp', 'tmp_repo', 'conf')
#         env.samples_dir = SAMPLESDIR
#         env.packages_dir = os.path.join(SAMPLESDIR, 'example_packages')
#         env.pcache = os.path.join('/', 'tmp', 'pcache')
#         env.distributions_path = os.path.join(env.micro_repository_path, 'distributions')
#         
#         with settings(command='mkdir -p %(micro_repository_conf)s' % env):
#             local('%(command)s' % env, capture=False)
#         
#         with settings(command='cp %(samples_dir)s/distributions\
#                   %(micro_repository_conf)s' % env):
#             local('%(command)s' % env, capture=False)
#             
#         with lcd('%(micro_repository_path)s' % env):
#             touch(env.distributions_path)
#             f = open(env.distributions_path, 'w')
#             f.write('kerepakupai dists/kerepakupai/Release')
#             f.close()
#             
#         with lcd('%(micro_repository_path)s' % env):
#             with settings(command='reprepro -VVV export'):
#                 local('%(command)s' % env, capture=False)
#                 
#         seed_packages = [('cube2font_1.2-2_i386.deb', 'main'), ('cube2font_1.2-2_amd64.deb', 'main'), 
#                          ('cl-sql-oracle_6.2.0-1_all.deb', 'no-libres'), ('libxine1-plugins_1.1.21-dmo2_all.deb', 'aportes'),
#                          ('acroread-debian-files_9.5.8_i386.deb', 'aportes'), ('acroread-debian-files_9.5.8_amd64.deb', 'aportes')]
#         
#         with lcd('%(micro_repository_path)s' % env):
#             for package, comp in seed_packages:
#                 with settings(command='reprepro -S %s includedeb %s %s/%s' %
#                              (comp, dist, env.packages_dir, package)):
#                     local('%(command)s' % env, capture=False)
#         
#         with lcd('%(micro_repository_path)s' % env):
#             create_cache(env.micro_repository_path, env.pcache)
#         
#         with lcd('%(micro_repository_path)s' % env):
#             fill_db_from_cache(env.pcache)
#         
#         add_list = [('libtacacs+1_4.0.4.26-3_amd64.deb', 'main'), ('libtacacs+1_4.0.4.26-3_i386.deb', 'main')]
#         update_list = [('cube2font_1.2-2_i386.deb', 'main'), ('cube2font_1.2-2_amd64.deb', 'main'), 
#                        ('libxine1-plugins_1.1.21-dmo2_all.deb', 'aportes')]
#         delete_list = [('cl-sql-oracle', 'no-libres'), ('acroread-debian-files', 'aportes'),
#                        ('acroread-debian-files', 'aportes')]
#         
#         with lcd('%(micro_repository_path)s' % env):
#             for package, comp in add_list:
#                 with settings(command='reprepro -S %s includedeb %s %s/%s' %
#                              (comp, dist, env.packages_dir, package)):
#                     local('%(command)s' % env, capture=False)
#             
#             for package, comp in update_list:
#                 with settings(command='reprepro -S %s includedeb %s %s/%s' %
#                              (comp, dist, env.packages_dir, package)):
#                     local('%(command)s' % env, capture=False)
#                     
#             for package, comp in delete_list:
#                 with settings(command='reprepro remove %s %s' % 
#                               (dist, package)):
#                     local('%(command)s' % env, capture=False)
#         
#         update_cache(env.micro_repository_path, env.pcache)
#         # FALTAN LOS ASSERT PARA VERIFICAR QUE LA ACTUALIZACION FUE CORRECTO
#         rmtree(env.micro_repository_path)
#         rmtree(env.pcache)


    def test_update_package_list(self):
        from tribus.common.recorder import record_paragraph, update_package_list
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        test_dist = "kukenan"
        old_amd_section = os.path.join(SAMPLESDIR, "Oldamd")
        old_i386_section = os.path.join(SAMPLESDIR, "Oldi386")
        new_amd_section = os.path.join(SAMPLESDIR, "Newamd.gz")
        new_i386_section = os.path.join(SAMPLESDIR, "Newi386.gz")
        
        for section in deb822.Packages.iter_paragraphs(open(old_amd_section)):
            record_paragraph(section, test_dist)
        for section in deb822.Packages.iter_paragraphs(open(old_i386_section)):
            record_paragraph(section, test_dist)
        
        update_package_list(new_amd_section, test_dist, 'i386')
        update_package_list(new_i386_section, test_dist, 'amd64')
        
        for section in deb822.Packages.iter_paragraphs(gzip.open(new_i386_section)):
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

        for section in deb822.Packages.iter_paragraphs(gzip.open(new_amd_section)):
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
            # Cuenta las relaciones pero no verifica que los datos guardados sean los correctos
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


    def test_fill_db_from_cache(self):
        pass
