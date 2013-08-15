import urllib
from debian import deb822
from recolector import Recolector

def registrarPaquetesBinarios(rutaArchivo, local = False):
    rec = Recolector()
    if local:
        archivo = file(rutaArchivo)
    else:
        archivo = urllib.urlopen(rutaArchivo)
    for paquete in deb822.Packages.iter_paragraphs(archivo):
        rec.crearPaquete(paquete)
        rec.mapearRelaciones(paquete)
        rec.mapearTags(paquete)
    rec.registrarRelaciones()
    rec.registrarTags()
    print "Finalizado"

def main():
    i386  = "http://10.16.106.152/repositorio/dists/waraira/main/binary-i386/Packages"
    amd64 = "http://10.16.106.152/repositorio/dists/waraira/main/binary-amd64/Packages"
    armel = "http://10.16.106.152/repositorio/dists/waraira/main/binary-armel/Packages"
    temp  = "http://10.16.106.152/repositorio/dists/waraira/main/binary-armel/Packages"
    registrarPaquetesBinarios(i386)
    registrarPaquetesBinarios(amd64)

main()