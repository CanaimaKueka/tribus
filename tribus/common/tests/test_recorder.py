#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

"""

These are the tests for the tribus.common.recorder module.

"""

import email.Utils
from debian import deb822
from django.test import TestCase
from tribus import BASEDIR
from tribus.common.utils import get_path
from tribus.web.cloud.models import Package, Details

SMPLDIR = get_path([BASEDIR, 'tribus', 'common', 'tests', 'samples'])
test_dist = 'kukenan'


class RecorderFunctions(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_update_paragraph(self):

        from tribus.common.recorder import update_paragraph
        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS

        old_paragraph = deb822.Packages(open(get_path([SMPLDIR, 'Blender'])))
        new_paragraph = deb822.Packages(open(get_path([SMPLDIR, 'BlenderNew'])))

        Package.objects.create_auto(old_paragraph, test_dist, 'main')
        update_paragraph(new_paragraph, test_dist, 'main')

        p = Package.objects.get(Name='blender')
        d = Details.objects.get(package=p)
        name, mail = email.Utils.parseaddr(new_paragraph.get('Maintainer'))
        total_relations = 0
        total_labels = 0

        self.assertEqual(p.Maintainer.Name, name)
        self.assertEqual(p.Maintainer.Email, mail)
        self.assertEqual(d.Distribution, test_dist)

        tag_list = new_paragraph['Tag'].replace('\n', '').split(', ')
        clean_list = [tuple(tag.split('::')) for tag in tag_list]

        for label in p.Labels.all():
            total_labels += 1
            self.assertIn((label.Name, label.Tags.Value), clean_list)

        self.assertEqual(total_labels, len(clean_list))

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

    # # TEST REDUNDANTE PERO NECESARIO (INCOMPLETO)
    # def test_update_cache(self):
    #     import urllib
    #     from tribus.common.iosync import rmtree
    #     from tribus.common.reprepro import create_repository, include_deb
    #     from tribus.common.recorder import fill_db_from_cache, create_cache

    #     pcache = os.path.join('/', 'tmp', 'pcache')
    #     tmp_repo = os.path.join('/', 'tmp', 'tmp_repo')
    #     dists_path = os.path.join(SMPLDIR, 'distributions')
    #     packages_dir = os.path.join(SMPLDIR, 'example_packages')

    #     source_seed_packages1 = 'http://paquetes.canaima.softwarelibre.gob.ve/pool'
    #     source_seed_packages2 = 'http://ftp.us.debian.org/debian/pool'

    #     list_seed_packages1 = [('main/c/cube2font',
    #                             'cube2font_1.2-2_i386.deb'),
    #                            ('main/c/cube2font',
    #                             'cube2font_1.2-2_amd64.deb'),
    #                            ('no-libres/c/cl-sql',
    #                             'cl-sql-oracle_6.2.0-1_all.deb'),
    #                            ('main/t/tacacs+',
    #                             'libtacacs+1_4.0.4.19-8_i386.deb'),
    #                            ('main/t/tacacs+',
    #                             'libtacacs+1_4.0.4.19-8_amd64.deb'),
    #                            ('aportes/a/acroread-debian-files',
    #                             'acroread-debian-files_9.5.8_i386.deb'),
    #                            ('aportes/a/acroread-debian-files',
    #                             'acroread-debian-files_9.5.8_amd64.deb')]

    #     list_seed_packages2 = [('main/c/cube2font',
    #                             'cube2font_1.3.1-2_i386.deb'),
    #                            ('main/c/cube2font',
    #                             'cube2font_1.3.1-2_amd64.deb'),
    #                            ('main/x/xine-lib',
    #                             'libxine1-plugins_1.1.19-2_all.deb'),
    #                            ('main/x/xine-lib',
    #                             'libxine1-plugins_1.1.21-1_all.deb')]

    #     for loc, name in list_seed_packages1:
    #         remote_path = os.path.join(source_seed_packages1, loc, name)
    #         local_path = os.path.join(packages_dir, name)
    #         try:
    #             urllib.urlretrieve(remote_path, local_path)
    #         except:
    #             print "No se pudo obtener una de las muestras, el test probablemente fallara"

    #     for loc, name in list_seed_packages2:
    #         remote_path = os.path.join(source_seed_packages2, loc, name)
    #         local_path = os.path.join(packages_dir, name)
    #         try:
    #             urllib.urlretrieve(remote_path, local_path)
    #         except:
    #             print "No se pudo obtener una de las muestras, el test probablemente fallara"

    #     create_repository(tmp_repo, dists_path)

    #     seed_packages = [('cube2font_1.2-2_i386.deb', 'main'),
    #                      ('cube2font_1.2-2_amd64.deb', 'main'),
    #                      ('cl-sql-oracle_6.2.0-1_all.deb', 'no-libres'),
    #                      ('libxine1-plugins_1.1.19-2_all.deb', 'main'),
    #                      ('acroread-debian-files_9.5.8_i386.deb', 'aportes'),
    #                      ('acroread-debian-files_9.5.8_amd64.deb', 'aportes')]

    #     with lcd(tmp_repo):
    #         for package, comp in seed_packages:
    #             include_deb(tmp_repo, comp, package)
    #         create_cache(tmp_repo, pcache)
    #         fill_db_from_cache(pcache)

    #     add_list = [('libtacacs+1_4.0.4.19-8_amd64.deb', 'main'),
    #                 ('libtacacs+1_4.0.4.19-8_i386.deb', 'main')]
    #     update_list = [('cube2font_1.3.1-2_i386.deb', 'main'),
    #                    ('cube2font_1.3.1-2_amd64.deb', 'main'),
    #                    ('libxine1-plugins_1.1.21-1_all.deb', 'main')]
    #     delete_list = [('cl-sql-oracle', 'no-libres'),
    #                    ('acroread-debian-files', 'aportes'),
    #                    ('acroread-debian-files', 'aportes')]

    #     with lcd(tmp_repo):
    #         for package, comp in add_list:
    #             include_deb(tmp_repo, comp, package)
    #         for package, comp in update_list:
    #             include_deb(tmp_repo, comp, package)
    #         for package, comp in delete_list:
    #             include_deb(tmp_repo, comp, package)

    #     #sync_cache(tmp_repo, pcache)
    #     # FALTAN LOS ASSERT PARA VERIFICAR QUE LA ACTUALIZACION FUE CORRECTA
    #     rmtree(tmp_repo)
    #     rmtree(pcache)

    # def test_create_cache(self):
    #     pass

    # # TEST COMPLETO PERO REDUNDANTE
    # def test_update_package_list(self):
    #     from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS

    #     old_amd_section = os.path.join(SMPLDIR, "Oldamd")
    #     old_i386_section = os.path.join(SMPLDIR, "Oldi386")
    #     new_amd_section = os.path.join(SMPLDIR, "Newamd")
    #     new_i386_section = os.path.join(SMPLDIR, "Newi386")
    #     new_amd_section_gz = os.path.join(SMPLDIR, "Newamd.gz")
    #     new_i386_section_gz = os.path.join(SMPLDIR, "Newi386.gz")

    #     for paragraph in deb822.Packages.iter_paragraphs(open(old_amd_section)):
    #         record_paragraph(paragraph, test_dist)
    #     for paragraph in deb822.Packages.iter_paragraphs(open(old_i386_section)):
    #         record_paragraph(paragraph, test_dist)

    #     amd_in = open(new_amd_section, 'rb')
    #     amd_out = gzip.open(os.path.join(SMPLDIR, 'Newamd.gz'), 'wb')
    #     amd_out.writelines(amd_in)
    #     amd_out.close()
    #     amd_in.close()

    #     i386_in = open(new_i386_section, 'rb')
    #     i386_out = gzip.open(os.path.join(SMPLDIR, 'Newi386.gz'), 'wb')
    #     i386_out.writelines(i386_in)
    #     i386_out.close()
    #     i386_in.close()

    #     update_package_list(new_i386_section_gz, test_dist, 'i386')
    #     update_package_list(new_amd_section_gz, test_dist, 'amd64')

    #     for paragraph in deb822.Packages.iter_paragraphs(gzip.open(new_i386_section_gz)):
    #         p = Package.objects.get(Name=paragraph['Package'])
    #         d = p.Details.get(package=p, Architecture=paragraph['Architecture'])
    #         name, mail = email.Utils.parseaddr(paragraph.get('Maintainer'))
    #         total_relations = 0

    #         self.assertEqual(p.Maintainer.Name, name)
    #         self.assertEqual(p.Maintainer.Email, mail)
    #         self.assertEqual(d.Distribution, test_dist)

    #         if paragraph.get('Tag'):
    #             tag_list = paragraph['Tag'].replace("\n", "").split(", ")
    #             clean_list = [tuple(tag.split("::")) for tag in tag_list]
    #             for label in p.Labels.all():
    #                 self.assertIn((label.Name, label.Tags.Value), clean_list)

    #         for field, field_db in PACKAGE_FIELDS.items():
    #             if paragraph.get(field):
    #                 self.assertEqual(str(getattr(p, field_db)), paragraph[field])

    #         for field, field_db in DETAIL_FIELDS.items():
    #             if paragraph.get(field):
    #                 self.assertEqual(str(getattr(d, field_db)), paragraph[field])

    #         for _, relations in paragraph.relations.items():
    #             if relations:
    #                 for relation in relations:
    #                     if len(relation) > 1:
    #                         for _ in relation:
    #                             total_relations += 1
    #                     else:
    #                         total_relations += 1

    #         self.assertEqual(d.Relations.all().count(), total_relations)

    #     for paragraph in deb822.Packages.iter_paragraphs(gzip.open(new_amd_section_gz)):
    #         p = Package.objects.get(Name=paragraph['Package'])
    #         d = p.Details.get(package=p, Architecture=paragraph['Architecture'])
    #         name, mail = email.Utils.parseaddr(paragraph.get('Maintainer'))
    #         total_relations = 0

    #         self.assertEqual(p.Maintainer.Name, name)
    #         self.assertEqual(p.Maintainer.Email, mail)
    #         self.assertEqual(d.Distribution, test_dist)

    #         if paragraph.get('Tag'):
    #             tag_list = paragraph['Tag'].replace("\n", "").split(", ")
    #             clean_list = [tuple(tag.split("::")) for tag in tag_list]
    #             for label in p.Labels.all():
    #                 self.assertIn((label.Name, label.Tags.Value), clean_list)

    #         for field, field_db in PACKAGE_FIELDS.items():
    #             if paragraph.get(field):
    #                 self.assertEqual(str(getattr(p, field_db)), paragraph[field])

    #         for field, field_db in DETAIL_FIELDS.items():
    #             if paragraph.get(field):
    #                 self.assertEqual(str(getattr(d, field_db)), paragraph[field])

    #         for _, relations in paragraph.relations.items():
    #             if relations:
    #                 for relation in relations:
    #                     if len(relation) > 1:
    #                         for _ in relation:
    #                             total_relations += 1
    #                     else:
    #                         total_relations += 1

    #         self.assertEqual(d.Relations.all().count(), total_relations)
