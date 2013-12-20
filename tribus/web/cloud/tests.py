#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email.Utils
import os
from django.test import TestCase
from debian import deb822
from tribus.web.cloud.models import *
from tribus.config.base import BASEDIR
from tribus.common.recorder import record_section, update_section, update_package_list

DISTRIBUTION = "Auyantepui"


class RecordTest(TestCase):

    def test_record_section(self):
        """
        Verifica si una seccion de un archivo Packages se registra correctamente en la
        base de datos.
        """
        print "\n###################"
        print "1. PRUEBA DE REGISTRO\n"

        packages_file = file(
            os.path.join(BASEDIR,
                         "tribus",
                         "web",
                         "cloud",
                         "test_files",
                         "Old"))

        for section in deb822.Packages.iter_paragraphs(packages_file, None, None, "windows-1252"):
            record_section(section, DISTRIBUTION)
            p = Package.objects.get(Package=section['Package'])
            d = Details.objects.get(
                package=p,
                Architecture=section['Architecture'],
                Distribution=DISTRIBUTION)
            rs = d.Relations
            relations_bd = len(rs.all())
            if 'Package' in section:
                self.assertEqual(p.Package, section['Package'])
            if 'Maintainer' in section:
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if 'Description' in section:
                self.assertEqual(p.Description, section['Description'])
            if 'Section' in section:
                self.assertEqual(p.Section, section['Section'])
            if 'Essential' in section:
                self.assertEqual(p.Essential, section['Essential'])
            if 'Priority' in section:
                self.assertEqual(p.Priority, section['Priority'])
            if 'Multi-Arch' in section:
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if 'Homepage' in section:
                self.assertEqual(p.Homepage, section['Homepage'])
            if 'Bugs' in section:
                self.assertEqual(p.Bugs, section['Bugs'])
            if 'Version' in section:
                self.assertEqual(d.Version, section['Version'])
            if 'Architecture' in section:
                self.assertEqual(d.Architecture, section['Architecture'])
            if 'Size' in section:
                self.assertEqual(str(d.Size), section['Size'])
            if 'Installed-Size' in section:
                self.assertEqual(
                    str(d.InstalledSize),
                    section['Installed-Size'])
            if 'MD5sum' in section:
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if 'Filename' in section:
                self.assertEqual(d.Filename, section['Filename'])

            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file += 1
                            exists = rs.filter(
                                relation_type=rel[0],
                                related_package__Package=rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1]
                                self.assertEqual(
                                    str(exists[0].relation),
                                    relation_version)
                                self.assertEqual(
                                    str(exists[0].version),
                                    number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(
                                    relation=rr['version'][0],
                                    version=rr['version'][1])
                                self.assertEqual(
                                    str(actual[0].version),
                                    rr['version'][1])
            self.assertEqual(relations_bd, relations_file)


class UpdateTest(TestCase):
    fixtures = ['base_fixture.json']

    def test_update_1_forward(self):
        print "\n###################"
        print "2. PRUEBA DE ACTUALIZACION FORWARD\n"
        updated_packages = file(
            os.path.join(BASEDIR,
                         "tribus",
                         "web",
                         "cloud",
                         "test_files",
                         "New"))
        for section in deb822.Packages.iter_paragraphs(updated_packages, None, None, "windows-1252"):
            update_section(section, DISTRIBUTION)
            p = Package.objects.get(Package=section['Package'])
            d = Details.objects.get(
                package=p,
                Architecture=section['Architecture'],
                Distribution=DISTRIBUTION)
            rs = d.Relations
            relations_bd = len(rs.all())
            if 'Package' in section:
                self.assertEqual(p.Package, section['Package'])
            if 'Maintainer' in section:
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if 'Description' in section:
                self.assertEqual(p.Description, section['Description'])
            if 'Section' in section:
                self.assertEqual(p.Section, section['Section'])
            if 'Essential' in section:
                self.assertEqual(p.Essential, section['Essential'])
            if 'Priority' in section:
                self.assertEqual(p.Priority, section['Priority'])
            if 'Multi-Arch' in section:
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if 'Homepage' in section:
                self.assertEqual(p.Homepage, section['Homepage'])
            if 'Bugs' in section:
                self.assertEqual(p.Bugs, section['Bugs'])
            if 'Version' in section:
                self.assertEqual(d.Version, section['Version'])
            if 'Architecture' in section:
                self.assertEqual(d.Architecture, section['Architecture'])
            if 'Size' in section:
                self.assertEqual(str(d.Size), section['Size'])
            if 'Installed-Size' in section:
                self.assertEqual(
                    str(d.InstalledSize),
                    section['Installed-Size'])
            if 'MD5sum' in section:
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if 'Filename' in section:
                self.assertEqual(d.Filename, section['Filename'])

            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file += 1
                            exists = rs.filter(
                                relation_type=rel[0],
                                related_package__Package=rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1]
                                self.assertEqual(
                                    str(exists[0].relation),
                                    relation_version)
                                self.assertEqual(
                                    str(exists[0].version),
                                    number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(
                                    relation=rr['version'][0],
                                    version=rr['version'][1])
                                self.assertEqual(
                                    str(actual[0].version),
                                    rr['version'][1])
            self.assertEqual(relations_bd, relations_file)

    def test_update_2_backward(self):
        print "\n###################"
        print "3. PRUEBA DE ACTUALIZACION BACKWARD\n"
        updated_packages = file(
            os.path.join(BASEDIR,
                         "tribus",
                         "web",
                         "cloud",
                         "test_files",
                         "Old"))
        for section in deb822.Packages.iter_paragraphs(updated_packages, None, None, "windows-1252"):
            update_section(section, DISTRIBUTION)
            p = Package.objects.get(Package=section['Package'])
            d = Details.objects.get(
                package=p,
                Architecture=section['Architecture'],
                Distribution=DISTRIBUTION)
            rs = d.Relations
            relations_bd = len(rs.all())
            if 'Package' in section:
                self.assertEqual(p.Package, section['Package'])
            if 'Maintainer' in section:
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if 'Description' in section:
                self.assertEqual(p.Description, section['Description'])
            if 'Section' in section:
                self.assertEqual(p.Section, section['Section'])
            if 'Essential' in section:
                self.assertEqual(p.Essential, section['Essential'])
            if 'Priority' in section:
                self.assertEqual(p.Priority, section['Priority'])
            if 'Multi-Arch' in section:
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if 'Homepage' in section:
                self.assertEqual(p.Homepage, section['Homepage'])
            if 'Bugs' in section:
                self.assertEqual(p.Bugs, section['Bugs'])
            if 'Version' in section:
                self.assertEqual(d.Version, section['Version'])
            if 'Architecture' in section:
                self.assertEqual(d.Architecture, section['Architecture'])
            if 'Size' in section:
                self.assertEqual(str(d.Size), section['Size'])
            if 'Installed-Size' in section:
                self.assertEqual(
                    str(d.InstalledSize),
                    section['Installed-Size'])
            if 'MD5sum' in section:
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if 'Filename' in section:
                self.assertEqual(d.Filename, section['Filename'])

            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file += 1
                            exists = rs.filter(
                                relation_type=rel[0],
                                related_package__Package=rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1]
                                self.assertEqual(
                                    str(exists[0].relation),
                                    relation_version)
                                self.assertEqual(
                                    str(exists[0].version),
                                    number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(
                                    relation=rr['version'][0],
                                    version=rr['version'][1])
                                self.assertEqual(
                                    str(actual[0].version),
                                    rr['version'][1])
            self.assertEqual(relations_bd, relations_file)

    def test_update_3_adding(self):
        print "\n###################"
        print "4. PRUEBA DE ACTUALIZACION ADDING\n"
        updated_packages = os.path.join(
            BASEDIR,
            "tribus",
            "web",
            "cloud",
            "test_files",
            "Old_More")
        packages_count = []
        for section in deb822.Packages.iter_paragraphs(file(updated_packages)):
            if section['Package'] not in packages_count:
                packages_count.append(section['Package'])
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            if rr['name'] not in packages_count:
                                packages_count.append(rr['name'])

        update_package_list(updated_packages, DISTRIBUTION)
        final_packages = len(Package.objects.all())
        self.assertEqual(len(packages_count), final_packages)

    def test_update_4_removing(self):
        print "\n###################"
        print "5. PRUEBA DE ACTUALIZACION REMOVING\n"
        updated_packages = os.path.join(
            BASEDIR,
            "tribus",
            "web",
            "cloud",
            "test_files",
            "Old_Less")
        packages_count = []
        for section in deb822.Packages.iter_paragraphs(file(updated_packages)):
            if section['Package'] not in packages_count:
                packages_count.append(section['Package'])
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            if rr['name'] not in packages_count:
                                packages_count.append(rr['name'])

        update_package_list(updated_packages, DISTRIBUTION)
        final_packages = len(Package.objects.all())
        self.assertNotEqual(len(packages_count), final_packages)
