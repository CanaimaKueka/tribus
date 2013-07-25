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
    i386 = "http://localhost/repositorio/dists/waraira/main/binary-i386/Packages"
    amd64 = "http://localhost/repositorio/dists/waraira/main/binary-amd64/Packages"
    registrarPaquetesBinarios(i386)
    registrarPaquetesBinarios(amd64)
    
main()