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
"""

#=========================================================================
# TODO:
# 1. Traducir documentación.
# 2. Explicar en la documentacion de los managers porque son necesarios,
#    cuales son los procedimientos especiales que justifican el uso
#    de un manejador personalizado.
#=========================================================================

# import os
# import logging
# from tribus import BASEDIR
from django.db import models
from email.Utils import parseaddr
from django.db.models import Q
from tribus.common.logger import get_logger
from tribus.config.pkgrecorder import PACKAGE_FIELDS, DETAIL_FIELDS

logger = get_logger()
# hdlr = logging.FileHandler(os.path.join(BASEDIR, 'tribus_recorder.log'))
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.INFO)


class MaintainerManager(models.Manager):

    def create_auto(self, maintainer_data):
        """

        Query the database for an existent maintainer.
        If it does not exist, create a new maintainer.

        :param maintainer_data: a string which contains maintainer's name and
                                email.
        :return: a `Maintainer` object.
        :rtype: ``Maintainer``

        .. versionadded:: 0.1

        """

        maintainer_name, maintainer_mail = parseaddr(maintainer_data)
        maintainer, _ = self.get_or_create(Name=maintainer_name,
                                           Email=maintainer_mail)
        return maintainer


class Maintainer(models.Model):
    """

    Representacion de un mantenedor de paquetes,
    constituida por su Nombre y Correo electronico.

    """
    objects = MaintainerManager()

    Name = models.CharField('nombre del mantenedor', max_length=100)
    Email = models.EmailField('correo electronico del mantenedor',
                              max_length=75)

    class Meta:
        ordering = ['Name']

    def __unicode__(self):
        return self.Name


class PackageManager(models.Manager):

    def create_auto(self, paragraph, branch, comp):
        """

        Queries the database for an existent package.
        If the package does exists but it doesn't have
        a maintainer, then the package data will be
        updated acording to the fields of the paragraph provided.
        If the package doesn't exists then it's created.

        :param paragraph: contains information about a binary package.
        :param branch: codename of the Canaima's version that will be updated.
        :param comp: component to which the paragraph belongs.
        :return: a `Package` object.
        :rtype: ``Package``

        .. versionadded:: 0.1

        """
        package, _ = self.get_or_create(Name=paragraph['Package'])

        if package.Maintainer:
            if not package.Details.filter(
                Distribution=branch, Component=comp).filter(
                    Q(Architecture=paragraph['Architecture']) |
                    Q(Architecture='all')):
                package.add_details(paragraph, branch, comp)

        else:
            for field, db_field in PACKAGE_FIELDS.items():
                setattr(package, db_field, paragraph.get(field))

            package.Maintainer = Maintainer.objects.create_auto(
                paragraph['Maintainer'])
            package.save()
            package.add_labels(paragraph)
            package.add_details(paragraph, branch, comp)

        return package


class Package(models.Model):
    """

    Representacion de los datos básicos de un paquete binario
    de acuerdo a la política de debian para manejo de paquetes:
    https://www.debian.org/doc/debian-policy/ch-controlfields.html

    Se consideran datos basicos aquellos que no varian según la
    arquitectura del paquete, existen otros campos que
    pueden incluirse en esta categoria, pero para los propositos
    de esta aplicación solo se consideran los siguientes:

    ['Package', 'Description', 'Homepage', 'Section',
     'Priority', 'Essential', 'Bugs', 'Multi-Arch']

    """
    objects = PackageManager()

    Name = models.CharField(
        'nombre del paquete', max_length=150)
    Maintainer = models.ForeignKey(
        Maintainer, verbose_name='nombre del mantenedor', null=True)
    Section = models.CharField(
        'seccion del paquete', max_length=50, null=True)
    Essential = models.CharField(
        'es esencial?', null=True, max_length=10)
    Priority = models.CharField(
        'prioridad del paquete', max_length=50, null=True)
    MultiArch = models.CharField(
        'multi-arquitectura', null=True, max_length=50)
    Description = models.TextField(
        'descripcion del paquete', max_length=500, null=True)
    Homepage = models.URLField(
        'pagina web del paquete', max_length=200, null=True)
    Bugs = models.CharField(
        'bugs existentes', null=True, max_length=200)
    Labels = models.ManyToManyField(
        'Label', null=True, symmetrical=False, blank=True)
    Details = models.ManyToManyField(
        'Details', null=True, symmetrical=False, blank=True)

    class Meta:
        ordering = ['Name']

    def __unicode__(self):
        return self.Name

    def update(self, paragraph, branch, comp):
        """

        Update the basic data of a package in the database.

        :param paragraph: contains information about a binary package.
        :param branch: codename of the Canaima's version that will be updated.
        :param comp: component to which the paragraph belongs.
        :return: a `Package` object.
        :rtype: ``Package``

        .. versionadded:: 0.1

        """
        for field, db_field in PACKAGE_FIELDS.items():
            setattr(self, db_field, paragraph.get(field))

        if not self.Maintainer:
            self.Maintainer = Maintainer.objects.create_maintainer(
                paragraph['Maintainer'])

        self.save()

        for label in self.Labels.all():
            self.Labels.remove(label)
            exists = Package.objects.filter(Labels=label)

            if not exists:
                label.delete()

        self.add_labels(paragraph)
        # Que pasa si no se encuentra el detalle?
        details = Details.objects.get(
            package=self, Architecture=paragraph.get('Architecture'),
            Distribution=branch, Component=comp)
        details.update(paragraph)

    def add_labels(self, paragraph):
        """

        Processes the contents of the 'Tag' field in the provided paragraph,
        records the labels into the database and relates them to a package.

        :param paragraph: contains information about a binary package.

        .. versionadded:: 0.2

        """
        if 'Tag' in paragraph:
            tag_list = paragraph['Tag'].replace('\n', '').split(', ')
            for tag in tag_list:
                tag_name, tag_value = tag.split('::')
                value, _ = Tag.objects.get_or_create(Value=tag_value)
                label, _ = Label.objects.get_or_create(
                    Name=tag_name, Tags=value)
                self.Labels.add(label)

    def add_details(self, paragraph, branch, comp):
        """
        Creates a new Details objects and relates it to the package.
        
        :param paragraph: contains information about a binary package.
        
        :param branch: codename of the Canaima's version that will be updated.
        
        :param comp: component to which the paragraph belongs.
        
        .. versionadded:: 0.2
        """
        
        details = Details.objects.create(Distribution=branch, Component = comp)
        for field, db_field in DETAIL_FIELDS.items():
            setattr(details, db_field, paragraph.get(field))
        details.save()
        details.add_relations(paragraph.relations.items())
        self.Details.add(details)
        logger.info('Adding new details to \'%s\' package in %s:%s ' %
                    (paragraph['package'], branch, paragraph['architecture']))
        return details
    
    
class Tag(models.Model):
    """
    Es cada uno de los valores que puede tener una etiqueta 
    en un paquete binario.
    Por ejemplo:
    
    La etiqueta 'implemented-in' puede tener uno o mas de
    los siguientes valores:
    
    ['java', 'python', 'C#']
    
    Cada uno de estos valores es un Tag.
    """
    
    Value = models.CharField("valor etiqueta", max_length=200)
    
    
    def __unicode__(self):
        return self.Value
    
    
class Label(models.Model):
    """
    Es una palabra o pequena frase que ayuda a identificar
    y/o caracterizar un paquete binario. Las etiquetas 
    proporcionan información sobre la funcion, origen,
    o prioridad de un paquete entre otras caracteristicas.
    Las etiquetas facilitan la clasificación de paquetes en
    multiples categorias, lo cual facilita su busqueda.
    
    Por ejemplo: 
    
    El paquete 0ad se puede encontrar buscando por alguna de 
    estas etiquetas:
    
    ['game', 'implemented-in', 'use']
    
    Una etiqueta puede estar asociada a uno o mas valores (Tags).
    """
    
    Name = models.CharField("nombre etiqueta", max_length=100)
    Tags = models.ForeignKey(Tag, null=True)
    
    
    def __unicode__(self):
        return self.Tags.Value
    
    
    class Meta:
        ordering = ["Name"]
    
    
class Relation(models.Model):
    """
    Representa los distintos lazos que relacionan un paquete
    con otro. Las relaciones entre paquetes se clasifican
    en los siguientes tipos:
    
    ["pre-depends", "depends", "recommends", "suggests",
     "provides", "enhances", "breaks", "replaces", "conflicts"]
     
    Una relacion debe indicar el tipo de relación, el paquete hacia
    el cual apunta la relación, la versión del paquete apuntado,
    el orden de la relación y opcionalmente el indice de los paquetes
    que son alternativa en la relación. Por ejemplo, un archivo de 
    control puede tener un parrafo con los siguientes datos:
    
    Name: blender
    Depends: libavcodec53 (>= 5:0.8-2~) | libavcodec-extra-53 (>= 5:0.8-2~) ...
    
    Donde:
    
    El paquete 'blender' tiene una relación de dependencia con el paquete 
    'libavcodec53' cuyo numero de versión sea mayor o igual a '5:0.8-2~', 
    ó, con el paquete 'libavcodec-extra-53' cuyo numero de version sea
    mayor o igual a '5:0.8-2~'.
    
    Para conocer mas sobre el siginificado de estas relaciones consulte:
    https://www.debian.org/doc/debian-policy/ch-relationships.html.
    """
    
    related_package = models.ForeignKey(Package, null=True, blank=True)
    version = models.CharField("numero de la version del paquete 'hijo'", 
        max_length=50, null=True, blank=True)
    order = models.CharField("orden de la version del paquete 'hijo'",
        max_length=75, null=True, blank=True)
    relation_type = models.CharField("orden de la version del paquete 'hijo'",
        max_length=75, null=True, blank=True)
    alt_id = models.IntegerField("indice de relacion con otros paquetes",
        null=True)
    
    
    def __unicode__(self):
        if self.order and self.version:
            return "%s (%s %s)" % (self.related_package.Name, self.order, self.version)
        else:
            return self.related_package.Name
    
    
class DetailsManager(models.Manager):
    def create_auto(self, paragraph, package, branch, comp):
        """
        Queries the database for the details of a given package.
        If there are no details then they are recorded.
    
        :param paragraph: contains information about a binary package.
    
        :param package: a `Package` object to which the details are related.
    
        :param branch: codename of the Canaima's version that will be recorded.
        
        :param comp: component to which the paragraph belongs.
    
        :return: a `Details` object.
    
        :rtype: ``Details``
    
        .. versionadded:: 0.2
        """
        
        try:
            return self.get(package=package,
                            Architecture=paragraph['Architecture'],
                            Distribution=branch, 
                            Component = comp)
        except Details.DoesNotExist:
            details = self.create(Distribution=branch, Component=comp)
            for field, db_field in DETAIL_FIELDS.items():
                setattr(details, db_field, paragraph.get(field))
            details.save()
            details.add_relations(paragraph.relations.items())
            package.Details.add(details)
            return details


class Details(models.Model):
    """
    Son aquellos campos cuyo valor varia según la arquitectura
    del paquete. Para los propositos de esta aplicación, los 
    campos tomados en cuenta son: 
    
    ["Version", "Architecture", "Size", "MD5sum", "Filename",
     "Installed-Size"]
    """
    
    Version = models.CharField("version del paquete", max_length=50, null=True)
    Architecture = models.CharField("arquitectura", max_length=75, null=True)
    Component = models.CharField("componente", max_length=75, null=True)
    Distribution = models.CharField("distribucion", max_length=75)
    Size = models.IntegerField("tamaño del paquete en esta arquitectura",
        null=True)
    InstalledSize = models.IntegerField(
        "tamaño una vez instalado en esta arquitectura", null=True)
    MD5sum = models.CharField("llave md5 del paquete en esta arquitectura",
        max_length=75, null=True)
    Filename = models.CharField("ruta del paquete en esta arquitectura",
        max_length=150, null=True)
    Relations = models.ManyToManyField('Relation', null=True, 
        symmetrical=False, blank=True)
    
    objects = DetailsManager()
    
    
    def __unicode__(self):
        if self.Architecture:
            return "%s : %s" % (self.Architecture, self.Distribution)
        
        
    def update(self, paragraph):
        """
        Updates the details of a Package in the database.
    
        :param paragraph: contains information about a binary package.
    
        :return: a `Details` object.
    
        :rtype: ``Details``
    
        .. versionadded:: 0.1
        """
        
        for field, db_field in DETAIL_FIELDS.items():
            setattr(self, db_field, paragraph.get(field))
        self.save()
        
        for relation in self.Relations.all():
            self.Relations.remove(relation)
            exists = Details.objects.filter(Relations=relation)
            if not exists:
                relation.delete()
        self.add_relations(paragraph.relations.items())
        
    
    def add_relation(self, relation_type, fields, alt_id=0):
        """
        Records a new relation in the database and then associates it to a `Details` object.
    
        :param relation_type: a string indicating the relationship type.
    
        :param fields: a dictionary which contains the relation information. Its structure is similar to::
    
                           {"name": "0ad-data", "version": (">=", "0~r11863"), "arch": None}
    
        :param alt_id: an integer used to relate a relation with its alternatives, e.g:
    
                           +----+-----------------+---------------+-----------+---------+--------+
                           | id | related_package | relation_type | relation  | version | alt_id |
                           +====+=================+===============+===========+=========+========+
                           |  1 |       23        |     depends   |    <=     |  0.98   |        |
                           +----+-----------------+---------------+-----------+---------+--------+
                           |  2 |       24        |     depends   |    >=     |  0.64   |    1   |
                           +----+-----------------+---------------+-----------+---------+--------+
                           |  3 |       25        |     depends   |    >=     |  2.76   |    1   |
                           +----+-----------------+---------------+-----------+---------+--------+
                           |  4 |       26        |     depends   |           |         |    1   |
                           +----+-----------------+---------------+-----------+---------+--------+
                           |  5 |       27        |     depends   |    <<     |  2.14   |        |
                           +----+-----------------+---------------+-----------+---------+--------+
    
                        in the above table, the relations with id 2, 3 and 4 are alternatives between
                        themselves because they have the same value in the field `alt_id`.
    
        .. versionadded:: 0.1
        """
        
        version = fields.get('version', None) 
        if version:
            order_version, number_version = version
        else:
            order_version, number_version = (None, None)
        related_package, _ = Package.objects.get_or_create(Name=fields['name'])
        new_relation, _ = Relation.objects.get_or_create(**{"related_package": related_package,
                                                            "relation_type": relation_type,
                                                            "order": order_version,
                                                            "version": number_version,
                                                            "alt_id": alt_id})
        self.Relations.add(new_relation)
    
    
    def add_relations(self, relations_list):
        """
        Records a set of relations associated to a `Details` object.
    
        :param relations_list: a list of tuples containing package relations to another packages.
                          Its structure is similar to::
    
                              [('depends', [[{'arch': None, 'name': u'libgl1-mesa-glx', 'version': None},
                              {'arch': None, 'name': u'libgl1', 'version': None}]],
                              [{'arch': None, 'name': u'0ad-data', 'version': (u'>=', u'0~r11863')}]), ('suggests', [])]
    
        .. versionadded:: 0.1
        """
        
        for relation_type, relations in relations_list:
            alt_id = 1
            if relations:
                for relation in relations:
                    if len(relation) > 1:
                        for relation_element in relation:
                            self.add_relation(relation_type,
                                                     relation_element, alt_id)
                        alt_id += 1
                    else:
                        self.add_relation(relation_type, relation[0])
