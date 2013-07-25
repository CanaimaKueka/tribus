# -*- coding: utf-8 -*-
from django.db import models
import string

class Mantenedor(models.Model):
    nombre_completo = models.CharField("nombre del mantenedor", max_length = 100)
    correo = models.EmailField("correo electronico del mantenedor", max_length= 75)
    
    def __unicode__(self):
        return self.nombre_completo
     
    class Meta:
        ordering = ["nombre_completo"]
        
class RelacionSimple(models.Model):
    dep = models.ForeignKey('Paquete')

    def __unicode__(self):
        return self.dep.Package

    class Meta:
        abstract = True
        ordering = ["dep"]
                
class DependenciaSimple(RelacionSimple):
    nombre = "cadena"

class PreDependenciaSimple(RelacionSimple):
    nombre = "cadena"

class RecomendacionSimple(RelacionSimple):
    nombre = "cadena"

class SugerenciaSimple(RelacionSimple):
    nombre = "cadena"

class ProveeSimple(RelacionSimple):
    nombre = "cadena"

class Mejora(RelacionSimple):
    nombre = "cadena"

class Rompe(RelacionSimple):
    nombre = "cadena"

class Reemplaza(RelacionSimple):
    nombre = "cadena"

class Conflicto(RelacionSimple):
    nombre = "cadena"

class RelacionOR(models.Model):
    
    def __unicode__(self): 
        x = ""
        for i in self.dep.only():
            x += i.dep.Package + " | "
        return string.strip(x, "| ")
        
    class Meta:
        abstract = True

class DependenciaOR(RelacionOR):
    dep = models.ManyToManyField(DependenciaSimple, null=True, symmetrical = False, blank=True)
    
class PreDependenciaOR(RelacionOR):
    dep = models.ManyToManyField(PreDependenciaSimple, null=True, symmetrical = False, blank=True)
    
class RecomendacionOR(RelacionOR):
    dep = models.ManyToManyField(RecomendacionSimple, null=True, symmetrical = False, blank=True)

class SugerenciaOR(RelacionOR):
    dep = models.ManyToManyField(SugerenciaSimple, null=True, symmetrical = False, blank=True)
    
class ProveeOR(RelacionOR):
    dep = models.ManyToManyField(ProveeSimple, null=True, symmetrical = False, blank=True)
    
class ValorTag(models.Model):
    valor = models.CharField("valor etiqueta", max_length = 100)
    
    def __unicode__(self):
        return self.valor
    
class Etiqueta(models.Model):
    nombre = models.CharField("nombre etiqueta", max_length = 100)
    valores = models.ForeignKey(ValorTag, null = True)
    
    def __unicode__(self):
        return self.valores.valor
     
    class Meta:
        ordering = ["nombre"]
    
class Paquete(models.Model):
    Package = models.CharField("nombre del paquete", max_length = 150)
    Version = models.CharField("version del paquete", max_length = 50, null = True)
    Size = models.IntegerField("tamaño del paquete", null = True)
    InstalledSize = models.IntegerField("tamaño una vez instalado", null = True)
    SHA256 = models.CharField("SHA256 del paquete", max_length = 100, null = True)
    SHA1 = models.CharField("SHA1", max_length = 100, null = True)
    MD5sum = models.CharField("llave md5 del paquete", max_length = 75, null = True)
    Description = models.TextField("descripcion del paquete", max_length = 200, null = True)
    Homepage = models.URLField("pagina web del paquete", max_length = 200, null = True)
    Descriptionmd5 = models.CharField("descripcion md5", max_length = 75, null = True)
    Maintainer = models.ForeignKey(Mantenedor, verbose_name = "nombre del mantenedor", null = True)
    Section = models.CharField("seccion del paquete", max_length = 50, null = True)
    Priority = models.CharField("prioridad del paquete", max_length = 50, null = True)
    Filename = models.CharField("nombre del archivo del paquete", max_length = 150, null = True)
    Architecture = models.CharField("arquitectura del paquete", null = True, max_length = 200)
    MultiArch = models.CharField("multi-arquitectura", null = True, max_length = 50)
    Essential = models.CharField("es esencial?", null = True, max_length = 10)
    Bugs = models.CharField("bugs existentes", null = True, max_length = 200)
    DependsS = models.ManyToManyField(DependenciaSimple, null=True, symmetrical = False, blank=True)
    DependsO = models.ManyToManyField(DependenciaOR, null=True, symmetrical = False, blank=True)
    PreDependsS = models.ManyToManyField(PreDependenciaSimple, null=True, symmetrical = False, blank=True)
    PreDependsO = models.ManyToManyField(PreDependenciaOR, null=True, symmetrical = False, blank=True)
    RecommendsS = models.ManyToManyField(RecomendacionSimple, null=True, symmetrical = False, blank=True)
    RecommendsO = models.ManyToManyField(RecomendacionOR, null=True, symmetrical = False, blank=True)
    SuggestsS = models.ManyToManyField(SugerenciaSimple, null=True, symmetrical = False, blank=True)
    SuggestsO = models.ManyToManyField(SugerenciaOR, null=True, symmetrical = False, blank=True)
    ProvidesS = models.ManyToManyField(ProveeSimple, null=True, symmetrical = False, blank=True)
    ProvidesO = models.ManyToManyField(ProveeOR, null=True, symmetrical = False, blank=True)
    Enhances = models.ManyToManyField(Mejora, null=True, symmetrical = False, blank=True)
    Breaks = models.ManyToManyField(Rompe, null=True, symmetrical = False, blank=True)
    Replaces = models.ManyToManyField(Reemplaza, null=True, symmetrical = False, blank=True)
    Conflicts = models.ManyToManyField(Conflicto, null=True, symmetrical = False, blank=True)
    Tags = models.ManyToManyField(Etiqueta, null=True, symmetrical = False, blank=True)
    
    class Meta:
        ordering = ["Package"]
    
    def __unicode__(self):
        return self.Package
    
class ListasPaquetes(models.Model):
    ruta = models.CharField("ruta del archivo", max_length = 150)
    md5actual = models.CharField("ruta del archivo", max_length = 150)