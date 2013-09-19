# -*- coding: utf-8 -*-
from django.db import models

class PackageList(models.Model):
    Path = models.CharField("ruta del archivo", max_length = 150)
    MD5 = models.CharField("ruta del archivo", max_length = 150)
    
class Maintainer(models.Model):
    Name = models.CharField("nombre del mantenedor", max_length = 100)
    Email = models.EmailField("correo electronico del mantenedor", max_length= 75)
    
    def __unicode__(self):
        return self.Name
    
    class Meta:
        ordering = ["Name"]
       
class Package(models.Model):
    Package = models.CharField("nombre del paquete", max_length = 150)
    Maintainer = models.ForeignKey(Maintainer, verbose_name = "nombre del mantenedor", null = True)
    Section = models.CharField("seccion del paquete", max_length = 50, null = True)
    Essential = models.CharField("es esencial?", null = True, max_length = 10)
    Priority = models.CharField("prioridad del paquete", max_length = 50, null = True)
    MultiArch = models.CharField("multi-arquitectura", null = True, max_length = 50)
    Description = models.TextField("descripcion del paquete", max_length = 500, null = True)
    Homepage = models.URLField("pagina web del paquete", max_length = 200, null = True)
    Bugs = models.CharField("bugs existentes", null = True, max_length = 200)
    Labels = models.ManyToManyField("Label", null=True, symmetrical = False, blank=True)
    Details = models.ManyToManyField("Details", null=True, symmetrical = False, blank=True)
    
    class Meta:
        ordering = ["Package"]
    
    def __unicode__(self):
        return self.Package
    
class Tag(models.Model):
    Value = models.CharField("valor etiqueta", max_length = 100)
     
    def __unicode__(self):
        return self.Value
    
class Label(models.Model):
    Name = models.CharField("nombre etiqueta", max_length = 100)
    Tags = models.ForeignKey(Tag, null = True)
    
    def __unicode__(self):
        return self.Tags.Value
    
    class Meta:
        ordering = ["Name"]
    
class Relation(models.Model):
    related_package = models.ForeignKey(Package, null=True, blank=True)
    relation = models.CharField("numero de la version del paquete 'hijo'", max_length = 50, null=True, blank=True)
    version = models.CharField("orden de la version del paquete 'hijo'", max_length = 75, null=True, blank=True)
    relation_type = models.CharField("orden de la version del paquete 'hijo'", max_length = 75, null=True, blank=True)
    alt_id = models.IntegerField("tamaño del paquete en esta arquitectura", null = True)
    
    def __unicode__(self):
        if self.relation and self.version:
            return self.related_package.Package  + " (" + self.relation + " " + self.version + ")"
        else:
            return self.related_package.Package
        
class Details(models.Model):
    Version = models.CharField("version del paquete", max_length = 50, null = True)
    Architecture = models.CharField("arquitectura", max_length = 75, null = True)
    Distribution = models.CharField("distribucion", max_length = 75, null = True)
    Size = models.IntegerField("tamaño del paquete en esta arquitectura", null = True)
    InstalledSize = models.IntegerField("tamaño una vez instalado en esta arquitectura", null = True)
    MD5sum = models.CharField("llave md5 del paquete en esta arquitectura", max_length = 75, null = True)
    Filename = models.CharField("ruta del paquete en esta arquitectura", max_length = 150, null = True)
    Relations = models.ManyToManyField('Relation', null=True, symmetrical = False, blank=True)
    
    def __unicode__(self):
        if self.Architecture:
            return self.Architecture  + " : " + self.Distribution
            