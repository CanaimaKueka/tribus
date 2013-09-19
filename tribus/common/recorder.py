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

tribus.common.recorder
===================

This module contains common functions to record package data from a repository.
Este modulo contiene funciones comunes para registrar datos de paquetes desde un repositorio.

'''

#===============================================================================
# TODO: 
# 1. Adaptar y probar los metodos de actualizacion de paquetes para esta estructura de tablas. COMPLETADO
# 2. Incluir registro de tags. COMPLETADO
# 3. Probablemente necesite actualizacion de tags. PENDIENTE
# 4. Organizar y ubicar funciones que aun no se donde deben ir. EN PROCESO 
# 5. Agregar registro de MD5 a la base de datos una vez se complete una actualizacion. COMPLETADO
# 6. Separar los procesos de actualizacion: 
# - Una tarea que se encargue de comparar y descargar la informacion de los archivos packages,
#   luego crear un directorio donde organizar los archivos descargados.
# - Una tarea para verificar el MD5 de los archivos Packages y actualizar dicha informacion en
#   la base de datos.
# 7. Documentar, documentar, documentar.
# 8. Hacer casos de prueba para los metodos criticos.
# 9. Un metodo en fabric para llenar la base de datos, sin romper otras cosas.
# 10. Agregar seccion para agregar nuevos paquetes durante las actualizaciones. COMPLETADO
# 11. Corregir descripcion de atributos en los modelos.
# 12. IDEA: Separar el registro y actualizacion en modulos distintos, permitiendo que el de actualizacion
#     tenga acceso al modulo de registro.
# 13. Parece necesario y correcto sustituir el None de las relacione simples por 0.
# 14. Eliminar paquetes obsoletos durante las actualizaciones. Actualmente no elimina los paquetes que ya
#     se registraron.
#===============================================================================

import urllib, urllib2, re, email.Utils, os, sys
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from django.db.models import Max
from tribus.web.paqueteria.models import *
from tribus.config.pkgrecorder import amd64, i386, package_fields, detail_fields, local, canaimai386

# TODO: Documentar
def record_maintainer(maintainer_data):
    name, mail = email.Utils.parseaddr(maintainer_data)
    exists = Maintainer.objects.filter(Name = name, Email = mail)
    if not exists:
        m = Maintainer(Name = name, Email = mail)
        m.save()
        return m
    else:
        return exists[0]

# TODO: Documentar, cambiar nombres poco intuitivos
def verify_fields(section, fields):
    d = {}
    for field in fields:
        if section.has_key(field):
            if "-" in field:
                d[field.replace("-", "")] = section[field]
            else:
                d[field] = section[field]
    return d

# TODO: Documentar
def find_package(name):
    exists = Package.objects.filter(Package = name)
    if exists:
        return exists[0]
    else:
        p = Package(Package = name)
        p.save()
        return p
    
# TODO: Documentar, cambiar nombres poco intuitivos
def record_package(section):
    exists = Package.objects.filter(Package = section['Package'])
    if exists:
        if not exists[0].Maintainer:
            print "Actualizando informacion de paquete"
            exists.update(**verify_fields(section, package_fields))
            p = Package.objects.filter(Package = section['Package'])[0]
            p.Maintainer = record_maintainer(section['Maintainer'])
            p.save()
            return p
        else:
            print "Usando paquete ya existente"
            return exists[0]
    else:
        print "Creando nuevo paquete"
        fields = verify_fields(section, package_fields)
        m = record_maintainer(section['Maintainer'])
        p = Package(**fields)
        p.Maintainer = m
        p.save()
        record_tags(section, p)
        return p

# TODO: Documentar, cambiar nombres poco intuitivos
def record_details(section, pq, dist = "kerepakupai"):
    exists = Details.objects.filter(package = pq,
                                    Architecture = section['Architecture'],
                                    Distribution = dist)
    if exists:
        return exists[0]
    else:
        fields = verify_fields(section, detail_fields)
        d = Details(**fields)
        d.Distribution = dist
        d.save()
        pq.Details.add(d)
        return d

# TODO: Documentar, cambiar nombres poco intuitivos
def create_relationship(fields):
    exists = Relation.objects.filter(**fields)
    if exists:
        return exists[0]
    else:
        obj = Relation(**fields)
        obj.save()
        return obj

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_relationship(dt, rtype, fields, alt_id = None):
    if fields['version']:
        rv = fields['version'][0]
        nv = fields['version'][1]
    else:
        rv = None
        nv = None
    related = find_package(fields['name'])
    new_rel = create_relationship({"related_package": related,
                                   "relation_type": rtype,
                                   "relation" : rv, "version": nv,
                                   "alt_id": alt_id})
    dt.Relations.add(new_rel)
 
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def create_tag(val):
    exists = Tag.objects.filter(Value = val)
    if exists:
        return exists[0]
    else:
        tag = Tag(Value = val)
        tag.save()
        return tag
    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def create_label(label_name, tag):
    exists = Label.objects.filter(Name = label_name, Tags = tag)
    if exists:
        return exists[0]
    else:
        label = Label(Name = label_name, Tags = tag)
        label.save()
        return label
        
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_relationships(detail, rtype, rels):
    limits = detail.Relations.filter(relation_type = rtype).aggregate(Max('alt_id'))
    M = limits['alt_id__max']
    if M:
        M += 1
    for r in rels:
        record_relationship(detail, rtype, r, M)
        
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def fix_index(pack, arch, rtype):
    val = Relation.objects.filter(details__package__Package = pack,
                                  details__Architecture = arch,
                                  relation_type = rtype,
                                  alt_id__gte = 1).values('alt_id')
    ind_list = []                              
    for n in val:
        if n.values()[0] not in ind_list:
            ind_list.append(n.values()[0])
    ind_list.reverse()
    total = len(ind_list)
    for el in range(1, total +1):
        print el
        Relation.objects.filter(details__package__Package = pack,
                                details__Architecture = arch,
                                relation_type = rtype,
                                alt_id = ind_list[el - 1]).update(**{'alt_id': el})
   
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_tags(section, pq):
    if section.has_key('Tag'):
        tag_list = section['Tag'].replace("\n", "").split(", ")
        for tag in tag_list:
            div_tag = tag.split("::")
            value = create_tag(div_tag[1])
            label = create_label(div_tag[0], value)
            pq.Labels.add(label)
                                          
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_section(section):
    p = record_package(section)
    d = record_details(section, p)
    for rel in section.relations.items():
        alt_id = 1
        if rel[1]:
            for r in rel[1]:
                pass
                if len(r) > 1:
                    for rr in r:
                        record_relationship(d, rel[0], rr, alt_id)
                    alt_id += 1
                else:
                    record_relationship(d, rel[0], r[0])
                    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def update_package(section):
    exists = Package.objects.filter(Package = section['Package'])
    exists.update(**verify_fields(section, package_fields))
    # Necesito encontrar una mejor forma de hacer esto: 
    # Actualizar los datos del paquete y mantener el objeto seleccionado 
    # para (en este caso) agregarle el mantenedor
    paquete = Package.objects.get(Package = section['Package'])
    if paquete.Maintainer.Name not in section['Maintainer'] or \
        paquete.Maintainer.Email not in section['Maintainer']: 
        paquete.Maintainer = record_maintainer(section['Maintainer'])
        paquete.save()
    return paquete

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def update_details(pq, section):
    exists = Details.objects.filter(package = pq,
                                    Architecture = section['Architecture'])
    exists.update(**verify_fields(section, detail_fields))
    exists[0].save()
    return exists[0]
    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def verify_obsolete(section, rtype, rel_bd):
    for relacion in rel_bd:
        found = False
        for name in section[rtype].replace(',', ' ').split():
            if re.match('^'+relacion.related_package.Package.replace("+", "\+").replace("-", "\-")+'$' , name):
                found = True
                break
        if not found:
            print "######"
            print "He detectado que esta relacion --> ", relacion
            print "no esta en el archivo Packages, por lo tanto la eliminare "
            relacion.delete()
            if relacion.alt_id != None:
                fix_index(section['Package'], section['Architecture'], rtype)

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def update_section(section):
    p = update_package(section)
    d = update_details(p, section)
    print "\nIniciando asistente de actualizacion"
    print "Actualizando la seccion -->", section['Package']
    for rel in section.relations.items():
        if rel[1]:
            existent_rel = Relation.objects.filter(details__package__Package = section['Package'],
                                                   details = d, relation_type = rel[0])
            verify_obsolete(section, rel[0], existent_rel)
            for r in rel[1]:
                for relation in r:
                    exists = Relation.objects.filter(related_package__Package = relation['name'],
                                                     details = d, relation_type = rel[0])
                    if exists and len(exists) == 1:
                        print "######"
                        print "He detectado que ya existe una relacion con el mismo nombre, que debo hacer?"
                        print relation
                        if relation['version']:
                            o, n = relation['version']
                            if exists[0].relation == o and exists[0].version != n:
                                print "Tiene el mismo orden, pero con una version distinta"
                                print "Actualizare la version de esta relacion -->", exists[0], n
                                exists[0].version = n
                                exists[0].save()
                            elif exists[0].relation != o:
                                print "Tiene orden distinto"
                                print "Registrare esta nueva relacion -->", relation
                                record_relationship(d, rel[0], relation)
                            elif exists[0].relation == o and exists[0].version == n:
                                print "El orden y la version son identicas, por lo tanto no hago nada =)"
                                print relation
                                print exists[0]
                            else:
                                print "Ha ocurrido un fallo en la logica del programador!"
                                print "Esta es la informacion que puedo suministrar:"
                                print relation
                                print exists[0]
                        else:
                            print "La relacion no tiene version y por lo tanto no debo hacer nada"
                            
                    elif exists and len(exists) > 1:
                        print "######"
                        print "He detectado que existen varias relaciones con el mismo nombre, que debo hacer?"
                        print relation
                        actual = exists.filter(relation = relation['version'][0])
                        if actual:
                            print "Selecciono la relacion coincidente con el orden"
                            print "Actualizare la version -->", actual[0], relation['version'][1]
                            actual[0].version = relation['version'][1]
                            actual[0].save()
                        else:
                            print "CDCNI: Caso desconocido y catastrofico no identificado"
                            print relation
                    else:
                        if len(r) > 1:
                            print "######"
                            print "He detectado que hay una relacion multiple sin registrar"
                            print "Procedere a registrarla"
                            record_relationships(d, rel[0], r)
                        else:
                            print "######"
                            print "No he encontrado la relacion en la base de datos, por lo tanto"
                            print "Registrare esta nueva relacion -->", relation
                            record_relationship(d, rel[0], relation)  
        else:
            listarelaciones = Relation.objects.filter(details = d, relation_type = rel[0])
            if listarelaciones:
                for relaciones in listarelaciones:
                    print "######"
                    print "He detectado que esta categoria ya no es valida, por lo tanto"
                    print "Eliminare los campos en esta categoria vacia -->", listarelaciones
                    relaciones.delete()

    print "Actualizacion finalizada"
    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def create_paths(raiz, distribuciones, componentes, arquitecturas):
    rutas = []
    for dist in distribuciones:
        for comp in componentes:
            for arq in arquitecturas:
                ruta = raiz + dist + "/" + comp + "/" + arq
                try:
                    urllib2.urlopen(ruta)
                    if arq != "source":
                        rutas.append(comp + "/" + arq + "/Packages")
                    else:
                        rutas.append(comp + "/" + arq + "/Sources")
                except:
                    print "La ruta", ruta, "no existe"
    return rutas

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_package_list(raiz, distribucion, rutas):
    listapaq = []
    datasource = urllib.urlopen(raiz + distribucion + "/Release")
    rel = deb822.Release(datasource)
    for l in rel['MD5Sum']:
        if l['name'] in rutas:
            listapaq.append((l['name'], l["md5sum"]))
    for lp in listapaq:
        existe = PackageList.objects.filter(Path = lp[0], MD5 = lp[1])
        if not existe:
            LP = PackageList(Path = lp[0], MD5 = lp[1])
            LP.save()

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def record_repository(raiz):
    rutas = create_paths(raiz, ["waraira"], ["main", "aportes", "no-libres"], 
                ["binary-i386", "binary-amd64", "binary-armel", "binary-armhf", "source"])
    record_package_list(raiz, "waraira", rutas)
    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def verify_package_list(raiz):
    archivosMod = []
    datasource = urllib.urlopen(raiz +  "/Release")
    rel = deb822.Release(datasource)
    for l in rel['MD5sum']:
        lp = PackageList.objects.filter(Path = l['name'])
        if lp:
            if lp[0].MD5 != l['md5sum']:
                archivosMod.append(l['name'])
    return archivosMod

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def update_package_list(raiz, ruta):
    datasource = urllib.urlopen(raiz + "/" + ruta)
    print raiz, ruta
    archivo = deb822.Packages.iter_paragraphs(datasource)
    print "Actualizando lista de paquetes"
    for section in archivo:
        existe = Details.objects.filter(package__Package = section['Package'], Architecture = section['Architecture'])
        if existe:
            if section['md5sum'] != existe[0].MD5sum:
                print "Se encontraron diferencias en la seccion -->", section['Package']
                print section['md5sum'], existe[0].MD5sum
                update_section(section)
                # Esto deberia ser un metodo pero aun no lo tengo claro
                new_md5 = ""
                datasource = urllib.urlopen(raiz +  "/Release")
                rel = deb822.Release(datasource)
                for l in rel['MD5sum']:
                    if l['name'] == ruta:
                        new_md5 = l['md5sum']
                path = PackageList.objects.filter(Path = ruta).update(MD5 = new_md5)
        else:
            record_section(section)
            print "Se estan agregando nuevos detalles"
            new_md5 = ""
            datasource = urllib.urlopen(raiz +  "/Release")
            rel = deb822.Release(datasource)
            for l in rel['MD5sum']:
                if l['name'] == ruta:
                    new_md5 = l['md5sum']
            path = PackageList.objects.filter(Path = ruta).update(MD5 = new_md5)
                    
# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def verify_updates():
    diff = verify_package_list(local + "waraira")
    if diff:
        mod1 = diff[0]
        print "Archivo con diferencias -->", mod1
        update_package_list(local + "waraira", mod1)
    else:
        print "No hay cambios en la lista de paquetes"

# TODO: Documentar, cambiar nombres poco intuitivos, terminar de traducir
def fill_database():
    file1 = urllib.urlopen(i386)
    file2 = urllib.urlopen(amd64)
    for section in deb822.Packages.iter_paragraphs(file1):
        record_section(section)
    for section in deb822.Packages.iter_paragraphs(file2):
        record_section(section)
    record_repository(local)
    