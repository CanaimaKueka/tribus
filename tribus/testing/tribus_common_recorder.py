# ===============================================================================
# VERIFICACION DE ACTUALIZACION
# ========================================================================

# import urllib
# import urllib2
# from debian import deb822
# from tribus.web.cloud.models import *
# import re


# def check_version(exists, rr, r):
#     if exists and len(exists) == 1:
#         if rr['version']:
#             o = rr['version'][0]
#             n = rr['version'][1]
#             if exists[0].relation == o and exists[0].version == n:
#                 print "=D", exists[0], "esta bien actualizado"
#             else:
#                 print "=C", exists[0], "no esta bien actualizado"
#                 print r
#         else:
#             print "=D", exists[0], "No tiene version, nada que verificar"
#     elif exists and len(exists) > 1:
#         actual = exists.filter(relation = rr['version'][0])
#         if actual:
#             print "=D", actual[0], "esta bien actualizado"
#         else:
#             print "=C", actual[0], "no esta bien actualizado"


# def comprobarActualizacion(paquete):
#     i386  = "http://10.16.106.152/repositorio/dists/waraira/main/binary-i386/Packages"
#     archivo = urllib.urlopen(i386)
#     relations_file = 0
#     print "Prueba numero 1: Verificacion de dependencias 1 a 1"
#     for section in deb822.Packages.iter_paragraphs(archivo):
#         if section['Package'] == paquete:

#             rels = Relation.objects.filter(details__package__Package = section['Package'],
#                                             details__Architecture = section['Architecture'])
#             relations_bd = len(rels)

#             for rel in section.relations.items():
#                 if rel[1]:
#                     for r in rel[1]:
#                         for rr in r:
#                             relations_file +=1
#                             exists = Relation.objects.filter(details__package__Package = section['Package'],
#                                                              details__Architecture = section['Architecture'],
#                                                              related_package__Package = rr['name'],
#                                                              relation_type = rel[0])
#                             check_version(exists, rr, r)
#             break

#     print "Prueba numero 2: Conteo de relaciones"
#     print "RELACIONES EN BD -->", relations_bd
#     print "RELACIONES EN ARCHIVO -->", relations_file

# def repeated_relation_counter():
#     i386  = "http://paquetes.canaima.softwarelibre.gob.ve/dists/kerepakupai/main/binary-i386/Packages"
#     archivo = urllib.urlopen(i386)
#     for section in deb822.Packages.iter_paragraphs(archivo):
#         for rel in section.relations.items():
#             if rel[1]:
#                 for r in rel[1]:
#                     for rr in r:
#                         encontrados = 0
#                         for name in section[rel[0]].replace(',', ' ').split():
#                             lista = re.match('^'+rr['name'].replace("+", "\+").replace("-", "\-")+'$', name)
#                             if lista and rr['version']:
#                                 encontrados += 1
#                         if encontrados > 2:
#                             print section['package']
#                             print r
