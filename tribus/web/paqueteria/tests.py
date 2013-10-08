#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email.Utils
from django.test import TestCase
from debian import deb822
from tribus.web.paqueteria.models import *
from tribus.common.recorder import record_section, record_package,\
    record_details, record_relationship, update_section

class RecordTest(TestCase):

    def test_record_section(self):
        """
        Verifica si una seccion de un archivo Packages se registra correctamente en la
        base de datos.
        """
        packages_file = file("tribus/web/paqueteria/test_files/Packages")        
        
        for section in deb822.Packages.iter_paragraphs(packages_file, None, None, "windows-1252"):
            record_section(section)
            p = Package.objects.get(Package = section['Package'])
            d = Details.objects.get(package = p, Architecture = section['Architecture'])
            rs = d.Relations
            relations_bd = len(rs.all())
            if section.has_key('Package'):
                self.assertEqual(p.Package, section['Package'])
            if section.has_key('Maintainer'):
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if section.has_key('Description'):
                self.assertEqual(p.Description, section['Description'])
            if section.has_key('Section'):
                self.assertEqual(p.Section, section['Section'])
            if section.has_key('Essential'):
                self.assertEqual(p.Essential, section['Essential'])
            if section.has_key('Priority'):
                self.assertEqual(p.Priority, section['Priority'])
            if section.has_key('Multi-Arch'):
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if section.has_key('Homepage'):
                self.assertEqual(p.Homepage, section['Homepage'])
            if section.has_key('Bugs'):
                self.assertEqual(p.Bugs, section['Bugs'])    
            if section.has_key('Version'):
                self.assertEqual(d.Version, section['Version'])
            if section.has_key('Architecture'):
                self.assertEqual(d.Architecture, section['Architecture'])
            if section.has_key('Size'):
                self.assertEqual(str(d.Size), section['Size'])
            if section.has_key('Installed-Size'):
                self.assertEqual(str(d.InstalledSize), section['Installed-Size'])
            if section.has_key('MD5sum'):
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if section.has_key('Filename'):
                self.assertEqual(d.Filename, section['Filename'])
            
            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file +=1
                            exists = rs.filter(relation_type = rel[0], related_package__Package = rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1] 
                                self.assertEqual(str(exists[0].relation), relation_version)
                                self.assertEqual(str(exists[0].version), number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(relation = rr['version'][0], 
                                                       version = rr['version'][1])
                                self.assertEqual(str(actual[0].version), rr['version'][1])
            self.assertEqual(relations_bd, relations_file)

class UpdateTest(TestCase):
    
    fixtures = ['paqueteria_before.json']
    
    def test_update_forward(self):
        updated_packages = file("tribus/web/paqueteria/test_files/PackagesNew")
        
        for section in deb822.Packages.iter_paragraphs(updated_packages, None, None, "windows-1252"):
            update_section(section)
            p = Package.objects.get(Package = section['Package'])
            d = Details.objects.get(package = p, Architecture = section['Architecture'])
            rs = d.Relations
            relations_bd = len(rs.all())
            if section.has_key('Package'):
                self.assertEqual(p.Package, section['Package'])
            if section.has_key('Maintainer'):
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if section.has_key('Description'):
                self.assertEqual(p.Description, section['Description'])
            if section.has_key('Section'):
                self.assertEqual(p.Section, section['Section'])
            if section.has_key('Essential'):
                self.assertEqual(p.Essential, section['Essential'])
            if section.has_key('Priority'):
                self.assertEqual(p.Priority, section['Priority'])
            if section.has_key('Multi-Arch'):
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if section.has_key('Homepage'):
                self.assertEqual(p.Homepage, section['Homepage'])
            if section.has_key('Bugs'):
                self.assertEqual(p.Bugs, section['Bugs'])    
            if section.has_key('Version'):
                self.assertEqual(d.Version, section['Version'])
            if section.has_key('Architecture'):
                self.assertEqual(d.Architecture, section['Architecture'])
            if section.has_key('Size'):
                self.assertEqual(str(d.Size), section['Size'])
            if section.has_key('Installed-Size'):
                self.assertEqual(str(d.InstalledSize), section['Installed-Size'])
            if section.has_key('MD5sum'):
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if section.has_key('Filename'):
                self.assertEqual(d.Filename, section['Filename'])
            
            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file +=1
                            exists = rs.filter(relation_type = rel[0], related_package__Package = rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1] 
                                self.assertEqual(str(exists[0].relation), relation_version)
                                self.assertEqual(str(exists[0].version), number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(relation = rr['version'][0], 
                                                       version = rr['version'][1])
                                self.assertEqual(str(actual[0].version), rr['version'][1])
            self.assertEqual(relations_bd, relations_file)
            
    def test_update_backward(self):
        updated_packages = file("tribus/web/paqueteria/test_files/Packages")
        
        for section in deb822.Packages.iter_paragraphs(updated_packages, None, None, "windows-1252"):
            update_section(section)
            p = Package.objects.get(Package = section['Package'])
            d = Details.objects.get(package = p, Architecture = section['Architecture'])
            rs = d.Relations
            relations_bd = len(rs.all())
            if section.has_key('Package'):
                self.assertEqual(p.Package, section['Package'])
            if section.has_key('Maintainer'):
                name, mail = email.Utils.parseaddr(section['Maintainer'])
                self.assertEqual(p.Maintainer.Name, name)
                self.assertEqual(p.Maintainer.Email, mail)
            if section.has_key('Description'):
                self.assertEqual(p.Description, section['Description'])
            if section.has_key('Section'):
                self.assertEqual(p.Section, section['Section'])
            if section.has_key('Essential'):
                self.assertEqual(p.Essential, section['Essential'])
            if section.has_key('Priority'):
                self.assertEqual(p.Priority, section['Priority'])
            if section.has_key('Multi-Arch'):
                self.assertEqual(p.MultiArch, section['Multi-Arch'])
            if section.has_key('Homepage'):
                self.assertEqual(p.Homepage, section['Homepage'])
            if section.has_key('Bugs'):
                self.assertEqual(p.Bugs, section['Bugs'])    
            if section.has_key('Version'):
                self.assertEqual(d.Version, section['Version'])
            if section.has_key('Architecture'):
                self.assertEqual(d.Architecture, section['Architecture'])
            if section.has_key('Size'):
                self.assertEqual(str(d.Size), section['Size'])
            if section.has_key('Installed-Size'):
                self.assertEqual(str(d.InstalledSize), section['Installed-Size'])
            if section.has_key('MD5sum'):
                self.assertEqual(d.MD5sum, section['MD5sum'])
            if section.has_key('Filename'):
                self.assertEqual(d.Filename, section['Filename'])
            
            relations_file = 0
            for rel in section.relations.items():
                if rel[1]:
                    for r in rel[1]:
                        for rr in r:
                            relations_file +=1
                            exists = rs.filter(relation_type = rel[0], related_package__Package = rr['name'])
                            if len(exists) == 1 and rr['version']:
                                relation_version = rr['version'][0]
                                number_version = rr['version'][1] 
                                self.assertEqual(str(exists[0].relation), relation_version)
                                self.assertEqual(str(exists[0].version), number_version)
                            elif len(exists) > 1 and rr['version']:
                                actual = exists.filter(relation = rr['version'][0], 
                                                       version = rr['version'][1])
                                self.assertEqual(str(actual[0].version), rr['version'][1])
            self.assertEqual(relations_bd, relations_file)