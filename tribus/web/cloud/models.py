# -*- coding: utf-8 -*-

#=========================================================================
# TODO:
# 1. Traducir documentación.
#=========================================================================

from django.db import models

# class MaintainerManager(models.Manager):
#     
#     @transaction.commit_manually
#     def record_maintainer(self, maintainer_data):
#         """
#         Queries the database for an existent maintainer.
#         If it does not exists, it creates a new maintainer.
#      
#         :param maintainer_data: a string which contains maintainer's name and
#         email.
#      
#         :return: a `Maintainer` object.
#      
#         :rtype: ``Maintainer``
#      
#         .. versionadded:: 0.1
#         """
#         
#         maintainer_name, maintainer_mail = email.Utils.parseaddr(maintainer_data)
#          
#         try:
#             maintainer, _ = Maintainer.objects.get_or_create(Name=maintainer_name,
#                                                              Email=maintainer_mail)
#         except DatabaseError, e:
#             transaction.rollback()
#             logger.info("There has been an error recording %s" % (maintainer_data))
#             logger.error(e.message)
#         else:
#             transaction.commit()
#             return maintainer


class Maintainer(models.Model):
    """
    Representacion de un mantenedor de paquetes,
    constituida por su Nombre y Correo electronico.
    """
    
    Name = models.CharField("nombre del mantenedor", max_length=100)
    Email = models.EmailField("correo electronico del mantenedor",
                              max_length=75)
    
    #objects = MaintainerManager()
    
    def __unicode__(self):
        return self.Name
    
    
    class Meta:
        ordering = ["Name"]


class Package(models.Model):
    """
    Representacion de los datos básicos de un paquete binario
    de acuerdo a la política de debian para manejo de paquetes: 
    https://www.debian.org/doc/debian-policy/ch-controlfields.html
    
    Se consideran datos basicos aquellos que no varian según la
    arquitectura del paquete, existen otros campos que
    pueden incluirse en esta categoria, pero para los propositos
    de esta aplicación solo se consideran los siguientes:   
    
    ["Package", "Description", "Homepage", "Section",
     "Priority", "Essential", "Bugs", "Multi-Arch"]
    """
    
    Name = models.CharField("nombre del paquete", max_length=150)
    Maintainer = models.ForeignKey(
        Maintainer,
        verbose_name="nombre del mantenedor",
        null=True)
    Section = models.CharField(
        "seccion del paquete",
        max_length=50,
        null=True)
    Essential = models.CharField("es esencial?", null=True, max_length=10)
    Priority = models.CharField(
        "prioridad del paquete",
        max_length=50,
        null=True)
    MultiArch = models.CharField(
        "multi-arquitectura",
        null=True,
        max_length=50)
    Description = models.TextField(
        "descripcion del paquete",
        max_length=500,
        null=True)
    Homepage = models.URLField(
        "pagina web del paquete",
        max_length=200,
        null=True)
    Bugs = models.CharField("bugs existentes", null=True, max_length=200)
    Labels = models.ManyToManyField(
        "Label",
        null=True,
        symmetrical=False,
        blank=True)
    Details = models.ManyToManyField(
        "Details",
        null=True,
        symmetrical=False,
        blank=True)

    class Meta:
        ordering = ["Name"]

    def __unicode__(self):
        return self.Name


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
    version = models.CharField(
        "numero de la version del paquete 'hijo'",
        max_length=50,
        null=True,
        blank=True)
    order = models.CharField(
        "orden de la version del paquete 'hijo'",
        max_length=75,
        null=True,
        blank=True)
    relation_type = models.CharField(
        "orden de la version del paquete 'hijo'",
        max_length=75,
        null=True,
        blank=True)
    alt_id = models.IntegerField(
        "tamaño del paquete en esta arquitectura",
        null=True)

    def __unicode__(self):
        if self.order and self.version:
            return "%s (%s %s)" % (self.related_package.Name, self.order, self.version)
        else:
            return self.related_package.Name


class Details(models.Model):
    """
    Son aquellos campos cuyo valor varia según la arquitectura
    del paquete. Para los propositos de esta aplicación, los 
    campos tomados en cuenta son: 
    
    ["Version", "Architecture", "Size", "MD5sum", "Filename",
     "Installed-Size"]
    """
    
    Version = models.CharField(
        "version del paquete",
        max_length=50,
        null=True)
    Architecture = models.CharField(
        "arquitectura",
        max_length=75,
        null=True)
    Distribution = models.CharField("distribucion", max_length=75)
    Size = models.IntegerField(
        "tamaño del paquete en esta arquitectura",
        null=True)
    InstalledSize = models.IntegerField(
        "tamaño una vez instalado en esta arquitectura",
        null=True)
    MD5sum = models.CharField(
        "llave md5 del paquete en esta arquitectura",
        max_length=75,
        null=True)
    Filename = models.CharField(
        "ruta del paquete en esta arquitectura",
        max_length=150,
        null=True)
    Relations = models.ManyToManyField(
        'Relation',
        null=True,
        symmetrical=False,
        blank=True)

    def __unicode__(self):
        if self.Architecture:
            return "%s : %s" % (self.Architecture, self.Distribution)
