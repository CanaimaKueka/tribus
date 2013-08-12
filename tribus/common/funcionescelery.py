import urllib, urllib2, os, sys
from debian import deb822
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from tribus.web.paqueteria.models import Paquete, ListasPaquetes
from tribus.common.recolector import *

def crearRutas(raiz, distribuciones, componentes, arquitecturas):
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
    
def registrarListasPaquetes(raiz, distribucion, rutas):
    listapaq = []
    datasource = urllib.urlopen(raiz + distribucion + "/Release")
    rel = deb822.Release(datasource)
    for l in rel['MD5Sum']:
        if l['name'] in rutas:
            listapaq.append((l['name'], l["md5sum"]))
    for lp in listapaq:
        existe = ListasPaquetes.objects.filter(ruta = lp[0], md5actual = lp[1])
        if not existe:
            LP = ListasPaquetes(ruta = lp[0], md5actual = lp[1])
            LP.save()
    
def verificarListasPaquetes(raiz):
    archivosMod = []
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
    datasource = urllib.urlopen(raiz + "/" + ruta)
    archivo = deb822.Packages.iter_paragraphs(datasource)
    for paq in archivo:
        existe = Paquete.objects.filter(Package = paq['Package'])
        if existe:
            print paq['md5sum'], existe[0].MD5sum
            if paq['md5sum'] != existe[0].MD5sum:
                pass
                

local = "http://localhost/repositorio/dists/"            
canaima = "http://paquetes.canaima.softwarelibre.gob.ve/dists/"

#rutas = crearRutas(local, ["waraira"], ["main", "aportes", "no-libres"], 
#               ["binary-i386", "binary-amd64", "binary-armel", "binary-armhf", "source"])
#registrarListasPaquetes(local, "waraira", rutas)

mod = verificarListasPaquetes(local + "waraira")
mod1 = mod[0]
print mod1

actualizarListaPaquetes(local + "waraira", mod1)
