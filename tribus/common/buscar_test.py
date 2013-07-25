import os, sys, email
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

from tribus.web.paqueteria.models import Mantenedor, Paquete, DependenciaOR, DependenciaSimple, RecomendacionSimple, \
ProveeSimple, SugerenciaSimple, PreDependenciaSimple, DependenciaOR, PreDependenciaOR, RecomendacionOR,\
SugerenciaOR, ProveeOR, Mejora, Rompe, Reemplaza, Conflicto, ValorTag, Etiqueta

objetos = {
        "mantenedor" : Mantenedor,
        "paquete" : Paquete,
        "depends" : DependenciaSimple,
        "recommends" : RecomendacionSimple,
        "provides" : ProveeSimple,
        "suggests" : SugerenciaSimple,
        "pre-depends" : PreDependenciaSimple,
        "dependsOR" : DependenciaOR,
        "pre-dependsOR" : PreDependenciaOR,
        "recommendsOR" : RecomendacionOR,
        "suggestsOR" : SugerenciaOR,
        "providesOR" : ProveeOR,
        "enhances" : Mejora,
        "breaks" : Rompe,
        "replaces" : Reemplaza,
        "conflicts" : Conflicto,
        "valorTag" : ValorTag,
        "etiqueta" : Etiqueta
    }

def buscarAtributos(atributo, datos = None, agregar = False):
    existe = objetos[atributo].objects.filter(**datos)
    if not existe:
        if agregar:
            if "OR" in atributo:
                obj = objetos[atributo]()
            else:
                obj = objetos[atributo](**datos)
            obj.save()
            return obj
        else:
            return False
    else:
        return existe[0]
    
def main():
    man = email.Utils.parseaddr("Debian Perl Group <pkg-perl-maintainers@lists.alioth.debian.org>")
    # Ejemplo de busqueda de mantenedor
    mant = buscarAtributos("mantenedor", {"nombre_completo": man[0],  "correo" : man[1]})
    print mant.nombre_completo
    print mant.correo
    # Ejemplo de busqueda de un paquete
    paquete = buscarAtributos("paquete", {"Package": "python2.7"})
    #paquete = buscarAtributos("paquete", {"Package": "blender", "Architecture" : "i386"})
    if paquete:
        print paquete.Package
        print paquete.Architecture
        # Ejemeplo de busqueda de dependencia simple
        dependencia = buscarAtributos("depends", {"dep": paquete})
        if dependencia:
            print "Encontre esta dependencia simple: ", dependencia
        # Ejemeplo de busqueda de dependencia OR
        depOR = buscarAtributos("dependsOR", {"dep__dep__Package": paquete})
        if depOR:
            print "Encontre esta dependencia OR: ", depOR
        sug = buscarAtributos("suggests", {"dep": paquete})
        if sug:
            print "Encontre esta sugerencia: ", sug
        
main()