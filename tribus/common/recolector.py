import email.Utils,os,sys
path = os.path.join(os.path.dirname(__file__), '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from tribus.web.paqueteria.models import *


class Recolector(object):
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
    
    necesarios = ["Package", "Version", "Size", "Installed-Size", "SHA256", "SHA1", "MD5sum", "Description", 
                  "Homepage", "Description-md5", "Section", "Priority", "Filename", "Architecture",
                  "Multi-Arch", "Essential", "Bugs"]
    
    def __init__(self):
        self.relaciones = {}
        self.etiquetas = {}
    
    def quitar_separador(self, cadena, sep):
        return string.join(string.splitfields(cadena, sep), "")
    
    def clonar_diccionario(self, paquete, necesarios):
        d = {}
        for i in paquete.items():
            if i[0] in necesarios:
                if "-" in i[0]:
                    d[str(self.quitar_separador(i[0], "-"))] = i[1]
                else:
                    d[str(i[0])] = i[1]    
        return d
    
    def buscarAtributos(self, atributo, datos = None, agregar = False):
        
        #
        #    BUSCA UN MANTENEDOR, SI AGREGRAR ES TRUE LO CREA
        #
        
        if atributo == "mantenedor":
            nombreMan, correoMan = email.Utils.parseaddr(datos)
            existe = self.objetos[atributo].objects.filter(nombre_completo = nombreMan, correo = correoMan)
            if not existe:
                Man = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
                if agregar:
                    Man.save()
                    return Man
                else: 
                    return 0
            else:
                return existe[0]
    
        #
        #    BUSCA UN ATRIBUTO, SI AGREGRAR ES TRUE LO CREA
        #
            
        else:
            existe = self.objetos[atributo].objects.filter(**datos)
            if existe:
                return existe[0]
            else:
            
            #
            #    AQUI SE AGREGAN LOS TIPOS DE ATRIBUTO 
            #    
                if agregar:
                    # Y ese 2 magico ahi que significa? 
                    if atributo[len(atributo)-2:len(atributo)] == "OR":
                        obj = self.objetos[atributo]()
                        obj.save()
                    else:
                        obj = self.objetos[atributo](**datos)
                        obj.save()
                    return obj
                return 0
            
    def crearPaquete(self, paquete):
        existe = self.buscarAtributos("paquete", {'Package' : paquete['Package'], 'Architecture' : paquete['Architecture']})
        if existe:
            return existe
        else:
            man = paquete['Maintainer']
            padap = self.clonar_diccionario(paquete, self.necesarios)
            nPaquete = Paquete(**padap)
            nPaquete.Maintainer = self.buscarAtributos("mantenedor", man, 1)
            nPaquete.save()
            return nPaquete
            
    def verificarRelaciones(self, rel):
        for r in rel.items():
            if r[1]:
                return True
        return False
        
    def mapearRelaciones(self, paquete):
        if self.verificarRelaciones(paquete.relations):
            self.relaciones[paquete['Package']] = {}
            for rel in paquete.relations.items():
                if rel[1]:
                    self.relaciones[paquete['Package']][rel[0]] = rel[1]
                    # Hack para guardar en memoria la architectura de cada paquete
                    self.relaciones[paquete['Package']].update({"arq": paquete['Architecture']})
    
    def mapearTags(self, paquete):
        if paquete.has_key('Tag'):    
            self.etiquetas[paquete['Package']] = string.splitfields(self.quitar_separador(paquete['Tag'], "\n"), ", ")
                    
    def registrarTags(self):
        for et in self.etiquetas.items():
            pq = Paquete.objects.get(Package = et[0])
            for t in et[1]:
                l = string.splitfields(t, "::")
                valor = self.buscarAtributos("valorTag", {"valor" : l[1]}, 1)
                etiqueta = self.buscarAtributos("etiqueta", {"nombre" : l[0], "valores" : valor}, 1)
                pq.Tags.add(etiqueta)
    
    def registrarRelaciones(self):
        for paquete in self.relaciones.items():
            arq = paquete[1].pop("arq") # Todos los paquetes deben tener registrado el campo arq
            pack = self.buscarAtributos("paquete", {"Package": paquete[0], "Architecture" : arq})
            for rel in paquete[1].items():
                for r in rel[1]:
                    if len(r) > 1:
                        ###### RELACIONES OR ###########
                        tipo = rel[0] + "OR"
                        rel_or = self.buscarAtributos(tipo, {"dep__dep__Package" : pack.Package},1)
                        if rel[0] == "depends":
                            pack.DependsO.add(rel_or)
                        elif rel[0] == "suggests":
                            pack.SuggestsO.add(rel_or)
                        elif rel[0] == "recommends":
                            pack.RecommendsO.add(rel_or)
                        elif rel[0] == "pre-depends":
                            pack.PreDependsO.add(rel_or)
                        elif rel[0] == "provides":
                            pack.ProvidesO.add(rel_or)
                        for ror in r:
                            pq = self.buscarAtributos("paquete",{"Package":ror['name']},1)
                            obj_rel = self.buscarAtributos(rel[0], {"dep": pq},1)
                            rel_or.dep.add(obj_rel)
                    else:
                        ###### RELACIONES SIMPLES ######
                        pq = self.buscarAtributos("paquete",{"Package":r[0]['name']},1)
                        obj_rel = self.buscarAtributos(rel[0], {"dep": pq},1)
                        if rel[0] == "depends":
                            pack.DependsS.add(obj_rel)
                        elif rel[0] == "suggests":
                            pack.SuggestsS.add(obj_rel)
                        elif rel[0] == "recommends":
                            pack.RecommendsS.add(obj_rel)
                        elif rel[0] == "pre-depends":
                            pack.PreDependsS.add(obj_rel)
                        elif rel[0] == "provides":
                            pack.ProvidesS.add(obj_rel)
                        elif rel[0] == "replaces":
                            pack.Replaces.add(obj_rel)
                        elif rel[0] == "enhances":
                            pack.Enhances.add(obj_rel)
                        elif rel[0] == "breaks":
                            pack.Breaks.add(obj_rel)
                        elif rel[0] == "replaces":
                            pack.Replaces.add(obj_rel)
                        elif rel[0] == "conflicts":
                            pack.Conflicts.add(obj_rel)