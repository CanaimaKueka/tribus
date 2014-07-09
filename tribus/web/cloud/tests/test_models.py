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

These are the tests for the tribus.web.cloud models.

"""

import os
from debian import deb822
from email.Utils import parseaddr
from django.test.testcases import TestCase
from tribus.web.cloud.models import (Maintainer, Package, Details, Relation)
from tribus.__init__ import BASEDIR
from tribus.common.utils import get_path

SAMPLESDIR = get_path([BASEDIR, 'tribus', 'common', 'tests', 'samples'])
test_dist = 'kukenan'


class RegistrationModelTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_maintainer_create(self):
        """
        El objetivo de este test es verificar que el registro de
        un mantenedor se haga correctamente.
        """

        maintainer_data = 'Super Mantenedor 86 <supermaintainer@86.com>'
        test_maintainer = Maintainer.objects.create_auto(maintainer_data)
        self.assertEqual(test_maintainer.Name, 'Super Mantenedor 86')
        self.assertEqual(test_maintainer.Email, 'supermaintainer@86.com')

    def test_package_create_auto(self):
        """
        El objetivo de este test es verificar que los campos basicos
        de un paquete sean registrados correctamente.
        """

        from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, 'Blender')))
        p = Package.objects.create_auto(paragraph, test_dist, 'main')
        d = Details.objects.get(package=p)
        total_relations = 0

        name, mail = parseaddr(paragraph.get('Maintainer'))

        self.assertEqual(d.Distribution, test_dist)
        self.assertEqual(p.Maintainer.Name, name)
        self.assertEqual(p.Maintainer.Email, mail)

        tag_list = paragraph['Tag'].replace('\n', '').split(', ')
        clean_list = [tuple(tag.split('::')) for tag in tag_list]

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

    def test_package_update(self):
        pass

    def test_package_add_labels(self):
        """
        El objetivo de este test es verificar que las etiquetas de un
        paquete se registran correctamente.
        """

        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, 'Blender')))
        package, _ = Package.objects.get_or_create(Name='blender')
        package.add_labels(paragraph)
        tag_list = paragraph['Tag'].replace('\n', '').split(', ')
        clean_list = [tuple(tag.split('::')) for tag in tag_list]
        for label in package.Labels.all():
            self.assertIn((label.Name, label.Tags.Value), clean_list)

    def test_package_add_details(self):
        pass

    def test_details_create(self):
        """
        El objetivo de este test es verificar que los campos de detalles
        sean registrados correctamente.
        """

        from tribus.config.pkgrecorder import DETAIL_FIELDS

        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        package, _ = Package.objects.get_or_create(Name='blender')
        details = Details.objects.create_auto(paragraph, package, test_dist, "main")
        self.assertEqual(details.Distribution, test_dist)

        for field, field_db in DETAIL_FIELDS.items():
            self.assertEqual(getattr(details, field_db), paragraph[field])

    def test_details_update(self):
        pass

    def test_details_add_relation(self):
        """
        El objetivo de este test es verificar que las relaciones
        se registren correctamente y de acuerdo al formato que maneja
        python-debian para archivos de control.
        """

        details, _ = Details.objects.get_or_create(Version='2.63a-1',
                                                   Architecture='i386',
                                                   Distribution=test_dist,
                                                   Component='main')
        reldata = [('depends', {'name': 'libc6',
                                'version': ('>=', '2.3.6-6~')}),
                   ('recommends', {'name': 'libpulse0',
                                   'version': ('>=', '0.9.21')}),
                   ('suggests', {'name': 'libportaudio2',
                                 'version': (None, None)})]

        for typerel, data in reldata:
            details.add_relation(typerel, data)

        for relation in details.Relations.all():
            self.assertIn((relation.relation_type,
                           {'name': relation.related_package.Name,
                            'version': (relation.order,
                                        relation.version)}), reldata)

        self.assertEqual(len(reldata), details.Relations.all().count())

    def test_details_add_relations(self):
        paragraph = deb822.Packages(open(os.path.join(SAMPLESDIR, "Blender")))
        details, _ = Details.objects.get_or_create(Version='2.63a-1',
                                                   Architecture='i386',
                                                   Distribution=test_dist)
        details.add_relations(paragraph.relations.items())
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
                            self.assertTrue(Relation.objects.get(
                                relation_type=relation_type,
                                related_package__Name=element['name'],
                                order=vo, version=vn))
                            total_relations += 1
                    else:
                        version = relation[0].get('version', None)
                        if version:
                            vo, vn = version
                        else:
                            vo, vn = (None, None)
                        self.assertTrue(Relation.objects.get(
                            relation_type=relation_type,
                            related_package__Name=relation[0]['name'],
                            order=vo, version=vn))
                        total_relations += 1
        self.assertEqual(details.Relations.all().count(), total_relations)
