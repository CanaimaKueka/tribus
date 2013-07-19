import email.Utils
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
    
    def buscar(self, tipo, dic):
        existe = self.objetos[tipo].objects.filter(**dic)
        if existe:
            return existe[0]
    
    def crearMantenedor(self, datos):
        nombreMan, correoMan = email.Utils.parseaddr(datos)
        existe = self.objetos["mantenedor"].objects.filter(nombre_completo = nombreMan, correo = correoMan)
        if existe:
            return existe[0]
        else:
            Man = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
            Man.save()
            return Man
    
    def crearPaquete(self, paquete):
        existe = self.objetos["paquete"].objects.filter(Package = paquete['Package'])
        if existe:
            return existe
        else:
            man = paquete['Maintainer']
            padap = self.clonar_diccionario(paquete, self.necesarios)
            nPaquete = self.objetos["paquete"](**padap)
            nPaquete.Maintainer = self.crearMantenedor(man)
            nPaquete.save()
            return nPaquete
        
    def buscarPaquete(self, nombre_pq):
        existe = Paquete.objects.filter(Package = nombre_pq)
        if existe:
            return existe[0]
        else:
            nPaquete = Paquete(Package = nombre_pq)
            nPaquete.save()
            return nPaquete
    
    def crearRelacionSimple(self, tipo, dic):
        existe = self.objetos[tipo].objects.filter(**dic)
        if existe:
            return existe[0]
        else:
            objeto = self.objetos[tipo](**dic)
            objeto.save()
            return objeto
    
    def crearRelacionOR(self, tipo, dic):
        existe = self.objetos[tipo].objects.filter(**dic)
        if existe:
            return existe[0]
        else:
            objeto = self.objetos[tipo]()
            objeto.save()
            return objeto
        
    def mapearRelaciones(self, paquete):
        self.relaciones[paquete['Package']] = {}
        for rel in paquete.relations.items():
            if rel[1]:
                self.relaciones[paquete['Package']][rel[0]] = rel[1]
                
    def mapearTags(self, paquete):
        if paquete.has_key('Tag'):    
            self.etiquetas[paquete['Package']] = string.splitfields(self.quitar_separador(paquete['Tag'], "\n"), ", ")
        
    def registrarTags(self):
        for et in self.etiquetas.items():
            pq = Paquete.objects.get(Package = et[0])
            for t in et[1]:
                l = string.splitfields(t, "::")
                valor = self.crearRelacionSimple("valorTag", {"valor" : l[1]})
                etiqueta = self.crearRelacionSimple("etiqueta", {"nombre" : l[0], "valores" : valor})
                pq.Tags.add(etiqueta)
    
    def registrarRelaciones(self):
        for paquete in self.relaciones.items():
            pack = self.buscar("paquete", {"Package": paquete[0]})
            for rel in paquete[1].items():
                for r in rel[1]:
                    if len(r) > 1:
                        ###### RELACIONES OR ###########
                        tipo = rel[0] + "OR"
                        rel_or = self.crearRelacionOR(tipo, {"dep__dep__Package" : pack.Package})
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
                            pq = self.buscarPaquete(ror['name'])
                            obj_rel = self.crearRelacionSimple(rel[0], {"dep": pq})
                            rel_or.dep.add(obj_rel)
                    else:
                        ###### RELACIONES SIMPLES ######
                        pq = self.buscarPaquete(r[0]['name'])
                        obj_rel = self.crearRelacionSimple(rel[0], {"dep": pq})
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