
import sys
import os

path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

import urllib
from debian import deb822
from tribus.common.recolector import Recolector
#from celerytest.models import ListasPaquetes
#from tribus.web.paqueteria.models import *


def main():
    rec = Recolector()
    #a1 = file('Packages')
    datasource = urllib.urlopen("http://localhost/repositorio/dists/waraira/main/binary-i386/Packages")
    for paquete in deb822.Packages.iter_paragraphs(datasource):
        rec.crearPaquete(paquete)
        rec.mapearRelaciones(paquete)
        rec.mapearTags(paquete)
    rec.registrarRelaciones()
    rec.registrarTags()
    print "Finalizado"
      
def registrarListasPaquetes():
    #raiz = "http://paquetes.canaima.softwarelibre.gob.ve/dists/kerepakupai/"
    raiz = "http://localhost/repositorio/dists/waraira/"
    datasource = urllib.urlopen(raiz + "/Release")
    secciones = ["main", "aportes", "no-libres"]
    archs = ["binary-i386", "binary-amd64", "binary-armel", "binary-armhf", "source"]
    listarutas = []
    listapaq = []
    for sec in secciones:
        for arq in archs:
            if arq != "source":
                listarutas.append(sec + "/" + arq + "/Packages")
            else:
                listarutas.append(sec + "/" + arq + "/Sources")
    rel = deb822.Release(datasource)
    
    for l in rel['MD5Sum']:
        if l['name'] in listarutas:
            listapaq.append((l['name'], l["md5sum"]))
    
    for lp in listapaq:
        existe = ListasPaquetes.objects.filter(ruta = lp[0], md5actual = lp[1])
        if not existe:
            LP = ListasPaquetes(ruta = lp[0], md5actual = lp[1])
            LP.save()
    
def verificarListasPaquetes():
    archivosMod = []
    raiz = "http://localhost/repositorio/dists/waraira/"
    datasource = urllib.urlopen(raiz + "/Release")
    rel = deb822.Release(datasource)
    for l in rel['MD5Sum']:
        lp = ListasPaquetes.objects.filter(ruta = l['name'])
        if lp:
            if lp[0].md5actual != l['md5sum']:
                archivosMod.append(l['name'])
    print archivosMod
    return archivosMod

def actualizarListaPaquetes(raiz, ruta):
    datasource = urllib.urlopen(raiz + ruta)
    archivo = deb822.Packages.iter_paragraphs(datasource)
    for paq in archivo:
        existe = Paquete.objects.filter(Package = paq['Package'])
        if existe:
            if paq['md5sum'] != existe[0].MD5sum:
                pass
main()
#registrarListasPaquetes()
#verificarListasPaquetes()
#actualizarListaPaquetes()