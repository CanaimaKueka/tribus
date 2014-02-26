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
from tribus.web.cloud.models import Package, Details,Relation

SAMPLESDIR = get_path([BASEDIR, "tribus", "testing", "samples" ])
test_dist = "kukenan"

class RecorderFunctions(TestCase):
    
    def setUp(self):
        pass        
        
        
    def tearDown(self):
        pass
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_maintainer(self):
        '''
        El objetivo de este test es verificar que el registro de
        un mantenedor se haga correctamente.
        '''
        
        from tribus.common.recorder import record_maintainer
        maintainer_data = "Super Mantenedor 86 <supermaintainer86@maintainer.com>"
        test_maintainer = record_maintainer(maintainer_data)
        self.assertEqual(test_maintainer.Name, "Super Mantenedor 86", "El nombre no coincide")
        self.assertEqual(test_maintainer.Email, "supermaintainer86@maintainer.com", "El correo no coincide")
    
    
#     Caso de prueba adicional en caso de registro con manejo de excepciones
#
#     def test_record_maintainer_exception(self):
#         from tribus.common.recorder import record_maintainer
#         from django.db import DatabaseError
#         maintainer_data = "Simón José Antonio de la Santísima Trinidad Bolívar y Ponte Palacios y Blanco <simonjoséantoniodelasantísimatrinidadbolívarypontepalaciosyblanco@simonjoséantoniodelasantísimatrinidadbolívarypontepalaciosyblanco.com"
#         self.assertRaises(DatabaseError, record_maintainer, maintainer_data)
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_package(self):
        '''
        El objetivo de este test es verificar que los campos basicos
        de un paquete sean registrados correctamente.
        '''
        
        from tribus.common.recorder import record_package
        from tribus.config.pkgrecorder import PACKAGE_FIELDS
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        package = record_package(paragraph)
        
        for field, field_db in PACKAGE_FIELDS.items():
            if paragraph.get(field):
                self.assertEqual(getattr(package, field_db), paragraph[field])
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_details(self):
        '''
        El objetivo de este test es verificar que los campos de detalles
        sean registrados correctamente.
        '''
        
        from tribus.common.recorder import record_details
        from tribus.config.pkgrecorder import DETAIL_FIELDS
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        package, _ = Package.objects.get_or_create(Name = 'blender')
        details = record_details(paragraph, package, test_dist)
        self.assertEqual(details.Distribution, test_dist)
        for field, field_db in DETAIL_FIELDS.items():
            self.assertEqual(getattr(details, field_db), paragraph[field])
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_tags(self):
        '''
        El objetivo de este test es verificar que las etiquetas de un
        paquete se registran correctamente.
        '''
        
        from tribus.common.recorder import record_tags
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        package, _ = Package.objects.get_or_create(Name = 'blender')
        record_tags(paragraph, package)
        tag_list = paragraph['Tag'].replace("\n", "").split(", ")
        clean_list = [tuple(tag.split("::")) for tag in tag_list]
        for label in package.Labels.all():
            self.assertIn((label.Name, label.Tags.Value), clean_list)
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_relationship(self):
        '''
        El objetivo de este test es verificar que las relaciones 
        se registren correctamente y de acuerdo al formato que maneja
        python-debian para archivos de control.
        '''
        
        from tribus.common.recorder import record_relationship
        details, _ = Details.objects.get_or_create(Version = '2.63a-1',
                                                   Architecture = 'i386',
                                                   Distribution = test_dist)
        reldata = [("depends", {"name": "libc6", "version": (">=", "2.3.6-6~")}),
                   ("recommends", {"name": "libpulse0", "version": (">=", "0.9.21")}),
                   ("suggests", {"name": "libportaudio2", "version": (None, None)})]
        
        for typerel, data in reldata:
            record_relationship(details, typerel, data)
        
        for relation in details.Relations.all():
            self.assertIn((relation.relation_type,
                           {"name": relation.related_package.Name,
                            "version": (relation.order, 
                                        relation.version)}), reldata)
        
        self.assertEqual(len(reldata), details.Relations.all().count())
    
    
    # TEST COMPLETO Y CORRECTO
    def test_record_relations(self):
        from tribus.common.recorder import record_relations
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        details, _ = Details.objects.get_or_create(Version = '2.63a-1',
                                                   Architecture = 'i386',
                                                   Distribution = test_dist)
        record_relations(details, paragraph.relations.items())
        total_relations = 0
        
        for relation_type, relations in paragraph.relations.items():
            if relations:
                for relation in relations:
                    if len(relation) > 1:
                        for element in relation:
                            version = element.get('version', None)
                            if version:
                                vo, vn = version
                            else:
                                vo, vn = (None, None)
                            self.assertTrue(Relation.objects.get(relation_type = relation_type,
                                            related_package__Name = element['name'],
                                            order = vo, version = vn))
                            total_relations += 1
                    else:
                        version = relation[0].get('version', None)
                        if version:
                            vo, vn = version
                        else:
                            vo, vn = (None, None)
                        self.assertTrue(Relation.objects.get(relation_type = relation_type,
                                        related_package__Name = relation[0]['name'],
                                        order = vo, version = vn))
                        total_relations += 1
        self.assertEqual(details.Relations.all().count(), total_relations)
    
    
    # TEST DE INTEGRACION COMPLETO Y CORRECTO
    def test_record_paragraph(self):
        from tribus.common.recorder import record_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        record_paragraph(paragraph, test_dist)
        p = Package.objects.get(Name = "blender")
        d = Details.objects.get(package = p)
        total_relations = 0
        name, mail = email.Utils.parseaddr(paragraph.get('Maintainer'))
        
        self.assertEqual(d.Distribution, test_dist)
        self.assertEqual(p.Maintainer.Name, name)
        self.assertEqual(p.Maintainer.Email, mail)
        
        tag_list = paragraph['Tag'].replace("\n", "").split(", ")
        clean_list = [tuple(tag.split("::")) for tag in tag_list]
        for label in p.Labels.all():
            self.assertIn((label.Name, label.Tags.Value), clean_list)
        
        for field, field_db in PACKAGE_FIELDS.items():
            if paragraph.get(field):
                self.assertEqual(str(getattr(p, field_db)), paragraph[field])
        
        for field, field_db in DETAIL_FIELDS.items():
            if paragraph.get(field):
                self.assertEqual(str(getattr(d, field_db)), paragraph[field])
        
        for _, relations in paragraph.relations.items():
            if relations:
                for relation in relations:
                    if len(relation) > 1:
                        for _ in relation:
                            total_relations += 1
                    else:
                        total_relations += 1
        
        self.assertEqual(d.Relations.all().count(), total_relations)
    
    
    # TEST DE INTEGRACION COMPLETO Y CORRECTO (REDUNDANDTE)
    def test_update_paragraph(self):
        from tribus.common.recorder import record_paragraph, update_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        
        old_paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        new_paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "BlenderNew")))
        
        record_paragraph(old_paragraph, test_dist)
        update_paragraph(new_paragraph, test_dist)
        
        p = Package.objects.get(Name = "blender")
        d = Details.objects.get(package = p)
        name, mail = email.Utils.parseaddr(new_paragraph.get('Maintainer'))
        total_relations = 0
        
        self.assertEqual(p.Maintainer.Name, name)
        self.assertEqual(p.Maintainer.Email, mail)
        self.assertEqual(d.Distribution, test_dist)
        
        tag_list = new_paragraph['Tag'].replace("\n", "").split(", ")
        clean_list = [tuple(tag.split("::")) for tag in tag_list]
        for label in p.Labels.all():
            self.assertIn((label.Name, label.Tags.Value),
                          clean_list)
        
        for field, field_db in PACKAGE_FIELDS.items():
            if new_paragraph.get(field):
                self.assertEqual(str(getattr(p, field_db)), new_paragraph[field])
        
        for field, field_db in DETAIL_FIELDS.items():
            if new_paragraph.get(field):
                self.assertEqual(str(getattr(d, field_db)), new_paragraph[field])
        
        for _, relations in new_paragraph.relations.items():
            if relations:
                for relation in relations:
                    if len(relation) > 1:
                        for _ in relation:
                            total_relations += 1
                    else:
                        total_relations += 1
        
        self.assertEqual(d.Relations.all().count(), total_relations)
    
    
    def test_create_cache(self):
        pass
    
    
    # TEST REDUNDANTE PERO NECESARIO (INCOMPLETO)
    def test_update_cache(self):
        import urllib
        from tribus.common.recorder import fill_db_from_cache, create_cache, update_cache
        from tribus.common.iosync import touch, rmtree
        env.samples_dir = SAMPLESDIR
        env.micro_repository_path = os.path.join('/', 'tmp', 'tmp_repo')
        env.micro_repository_conf = os.path.join('/', 'tmp', 'tmp_repo', 'conf')
        env.packages_dir = os.path.join(SAMPLESDIR, 'example_packages')
        env.pcache = os.path.join('/', 'tmp', 'pcache')
        env.distributions_path = os.path.join(env.micro_repository_path, 'distributions')
        
        source_seed_packages1 = 'http://paquetes.canaima.softwarelibre.gob.ve/pool'
        source_seed_packages2 = 'http://ftp.us.debian.org/debian/pool'
        
        list_seed_packages1 = [('main/c/cube2font', 'cube2font_1.2-2_i386.deb'),
                               ('main/c/cube2font', 'cube2font_1.2-2_amd64.deb'),
                               ('no-libres/c/cl-sql', 'cl-sql-oracle_6.2.0-1_all.deb'),
                               ('main/t/tacacs+', 'libtacacs+1_4.0.4.19-8_i386.deb'),
                               ('main/t/tacacs+', 'libtacacs+1_4.0.4.19-8_amd64.deb'),
                               ('aportes/a/acroread-debian-files', 'acroread-debian-files_9.5.8_i386.deb'),
                               ('aportes/a/acroread-debian-files', 'acroread-debian-files_9.5.8_amd64.deb')]
        
        list_seed_packages2 = [('main/c/cube2font', 'cube2font_1.3.1-2_i386.deb'),
                               ('main/c/cube2font', 'cube2font_1.3.1-2_amd64.deb'),
                               ('main/x/xine-lib', 'libxine1-plugins_1.1.19-2_all.deb'),
                               ('main/x/xine-lib', 'libxine1-plugins_1.1.21-1_all.deb')]
        
        for loc, name in list_seed_packages1:
            remote_path = os.path.join(source_seed_packages1, loc, name)
            local_path = os.path.join(env.packages_dir, name)
            try:
                urllib.urlretrieve(remote_path, local_path)
            except:
                print "No se pudo obtener una de las muestras, el test probablemente fallara"
        
        for loc, name in list_seed_packages2:
            remote_path = os.path.join(source_seed_packages2, loc, name)
            local_path = os.path.join(env.packages_dir, name)
            try:
                urllib.urlretrieve(remote_path, local_path)
            except:
                print "No se pudo obtener una de las muestras, el test probablemente fallara"
        
        with settings(command='mkdir -p %(micro_repository_conf)s' % env):
            local('%(command)s' % env, capture=False)
        
        with settings(command='cp %(samples_dir)s/distributions\
                  %(micro_repository_conf)s' % env):
            local('%(command)s' % env, capture=False)
        
        with lcd('%(micro_repository_path)s' % env):
            touch(env.distributions_path)
            f = open(env.distributions_path, 'w')
            f.write('kukenan dists/kukenan/Release')
            f.close()
        
        with lcd('%(micro_repository_path)s' % env):
            with settings(command='reprepro -VVV export'):
                local('%(command)s' % env, capture=False)
        
        seed_packages = [('cube2font_1.2-2_i386.deb', 'main'), ('cube2font_1.2-2_amd64.deb', 'main'), 
                         ('cl-sql-oracle_6.2.0-1_all.deb', 'no-libres'), ('libxine1-plugins_1.1.19-2_all.deb', 'main'),
                         ('acroread-debian-files_9.5.8_i386.deb', 'aportes'), ('acroread-debian-files_9.5.8_amd64.deb', 'aportes')]
        
        with lcd('%(micro_repository_path)s' % env):
            for package, comp in seed_packages:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, test_dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
        
        with lcd('%(micro_repository_path)s' % env):
            create_cache(env.micro_repository_path, env.pcache)
        
        with lcd('%(micro_repository_path)s' % env):
            fill_db_from_cache(env.pcache)
        
        add_list = [('libtacacs+1_4.0.4.19-8_amd64.deb', 'main'), ('libtacacs+1_4.0.4.19-8_i386.deb', 'main')]
        update_list = [('cube2font_1.3.1-2_i386.deb', 'main'), ('cube2font_1.3.1-2_amd64.deb', 'main'), 
                       ('libxine1-plugins_1.1.21-1_all.deb', 'main')]
        delete_list = [('cl-sql-oracle', 'no-libres'), ('acroread-debian-files', 'aportes'),
                       ('acroread-debian-files', 'aportes')]
        
        with lcd('%(micro_repository_path)s' % env):
            for package, comp in add_list:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, test_dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
            
            for package, comp in update_list:
                with settings(command='reprepro -S %s includedeb %s %s/%s' %
                             (comp, test_dist, env.packages_dir, package)):
                    local('%(command)s' % env, capture=False)
            
            for package, comp in delete_list:
                with settings(command='reprepro remove %s %s' % 
                              (test_dist, package)):
                    local('%(command)s' % env, capture=False)
        
        update_cache(env.micro_repository_path, env.pcache)
        # FALTAN LOS ASSERT PARA VERIFICAR QUE LA ACTUALIZACION FUE CORRECTA
        rmtree(env.micro_repository_path)
        rmtree(env.pcache)
    
    
    # TEST COMPLETO PERO REDUNDANTE
    def test_update_package_list(self):
        from tribus.common.recorder import record_paragraph, update_package_list
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        
        old_amd_section = os.path.join(SAMPLESDIR, "Oldamd")
        old_i386_section = os.path.join(SAMPLESDIR, "Oldi386")
        new_amd_section = os.path.join(SAMPLESDIR, "Newamd")
        new_i386_section = os.path.join(SAMPLESDIR, "Newi386")
        new_amd_section_gz = os.path.join(SAMPLESDIR, "Newamd.gz")
        new_i386_section_gz = os.path.join(SAMPLESDIR, "Newi386.gz")
        
        for paragraph in deb822.Packages.iter_paragraphs(open(old_amd_section)):
            record_paragraph(paragraph, test_dist)
        for paragraph in deb822.Packages.iter_paragraphs(open(old_i386_section)):
            record_paragraph(paragraph, test_dist)
        
        amd_in = open(new_amd_section, 'rb')
        amd_out = gzip.open(os.path.join(SAMPLESDIR, 'Newamd.gz'), 'wb')
        amd_out.writelines(amd_in)
        amd_out.close()
        amd_in.close()
        
        i386_in = open(new_i386_section, 'rb')
        i386_out = gzip.open(os.path.join(SAMPLESDIR, 'Newi386.gz'), 'wb')
        i386_out.writelines(i386_in)
        i386_out.close()
        i386_in.close()
        
        update_package_list(new_i386_section_gz, test_dist, 'i386')
        update_package_list(new_amd_section_gz, test_dist, 'amd64')
        
        for paragraph in deb822.Packages.iter_paragraphs(gzip.open(new_i386_section_gz)):
            p = Package.objects.get(Name = paragraph['Package'])
            d = p.Details.get(package = p, Architecture = paragraph['Architecture'])
            name, mail = email.Utils.parseaddr(paragraph.get('Maintainer'))
            total_relations = 0
            
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
            self.assertEqual(d.Distribution, test_dist)
            
            if paragraph.get('Tag'):
                tag_list = paragraph['Tag'].replace("\n", "").split(", ")
                clean_list = [tuple(tag.split("::")) for tag in tag_list]
                for label in p.Labels.all():
                    self.assertIn((label.Name, label.Tags.Value), clean_list)
            
            for field, field_db in PACKAGE_FIELDS.items():
                if paragraph.get(field):
                    self.assertEqual(str(getattr(p, field_db)), paragraph[field])
        
            for field, field_db in DETAIL_FIELDS.items():
                if paragraph.get(field):
                    self.assertEqual(str(getattr(d, field_db)), paragraph[field])
            
            for _, relations in paragraph.relations.items():
                if relations:
                    for relation in relations:
                        if len(relation) > 1:
                            for _ in relation:
                                total_relations += 1
                        else:
                            total_relations += 1
            
            self.assertEqual(d.Relations.all().count(), total_relations)
        
        
        for paragraph in deb822.Packages.iter_paragraphs(gzip.open(new_amd_section_gz)):
            p = Package.objects.get(Name = paragraph['Package'])
            d = p.Details.get(package = p, Architecture = paragraph['Architecture'])
            name, mail = email.Utils.parseaddr(paragraph.get('Maintainer'))
            total_relations = 0
            
            self.assertEqual(p.Maintainer.Name, name)
            self.assertEqual(p.Maintainer.Email, mail)
            self.assertEqual(d.Distribution, test_dist)
            
            if paragraph.get('Tag'):
                tag_list = paragraph['Tag'].replace("\n", "").split(", ")
                clean_list = [tuple(tag.split("::")) for tag in tag_list]
                for label in p.Labels.all():
                    self.assertIn((label.Name, label.Tags.Value), clean_list)
            
            for field, field_db in PACKAGE_FIELDS.items():
                if paragraph.get(field):
                    self.assertEqual(str(getattr(p, field_db)), paragraph[field])
            
            for field, field_db in DETAIL_FIELDS.items():
                if paragraph.get(field):
                    self.assertEqual(str(getattr(d, field_db)), paragraph[field])
            
            for _, relations in paragraph.relations.items():
                if relations:
                    for relation in relations:
                        if len(relation) > 1:
                            for _ in relation:
                                total_relations += 1
                        else:
                            total_relations += 1
            
            self.assertEqual(d.Relations.all().count(), total_relations)


    def test_fill_db_from_cache(self):
        pass
