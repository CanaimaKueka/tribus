import os
import urllib
from tribus.common.iosync import rmtree
from debian import deb822

# Con esto puedo crear una carpeta de cache a a partir de los nombres de cada distribucion o rama

repo_root = 'http://paquetes.canaima.softwarelibre.gob.ve'
local = '/tmp/cache'
branches = ['aponwao', 'auyantepui', 'roraima', 'kerepakupai', 'kukenan']


if not os.path.isdir(local):
    os.makedirs(local)
    
for branch in branches:
    remote_branch_path = os.path.join(repo_root, "dists", branch)
    local_branch_path = os.path.join(local, branch)
    release_data = urllib.urlopen(os.path.join(repo_root, "dists", branch, "Release"))
    release_control_file = deb822.Release(release_data)
    
    archs = release_control_file.get('Architectures').split()
    comps = release_control_file.get('Components').split()
    md5sums = release_control_file.get('MD5Sum')
    
    #print md5sums
    
    for comp in comps:
        for arch in archs:
            # if md5sum.get('name') == os.path.join(comp, 'binary-' + arch, 'Packages.gz'):
                
            remote_file_path = os.path.join(remote_branch_path, comp, 'binary-' + arch)
            local_file_path = os.path.join(local_branch_path, comp, 'binary-' + arch)
            
            #for md5sum in md5sums:
            #    if md5sum.get('name') == os.path.join(comp, 'binary-' + arch, 'Packages.gz'):
            #        print md5sum
                    
            
            #if not os.path.isdir(local_file_path):
            #    os.makedirs(local_file_path)
    
rmtree(local)


# METODOS ALTERNATIVOS PARA REGISTRAR PAQUETES
# def setear_objeto(obj, section, fields):
#     """
#     Intento de abstraer la logica para crear y
#     actualizar objetos a partir de un archivo de control 
#     y una lista de los campos considerados
#     """
#     
#     for field in fields:
#         setattr(obj,
#                 field.replace("-", "") if "-" in field else field, 
#                 section.get(field, None))
#     return obj

# def alt_record_package(section):
#     """
#     Alternativa para registrar paquetes en base de datos
#     sin necesidad de seleccionar previamente los campos en
#     un diccionario separado.
#     Falta depurar y mejorar algunas cosas
#     
#     """
#     
#     exists = Package.objects.filter(Package=section['Package'])
#     if exists:
#         p = exists[0]
#         if not p.Maintainer:
#             p = setear_objeto(p, section, package_fields)
#             p.Maintainer = record_maintainer(section['Maintainer'])
#             p.save()
#             return p
#         else:
#             return p
#     else:
#         p = setear_objeto(Package(), section, package_fields)
#         m = record_maintainer(section['Maintainer'])
#         p.Maintainer = m
#         p.save()
#         record_tags(section, p)
#         return p
# FIN METODOS ALTERNATIVOS


# def create_cache_dir_alt(repository_root, cache_dir_path):
#     branches = ['aponwao', 'auyantepui', 'roraima', 'kerepakupai', 'kukenan']
#     
#     for branch in branches:
#         remote_branch_path = os.path.join(repository_root, "dists", branch)
#         local_branch_path = os.path.join(repository_root, branch)
#         release_data = urllib.urlopen(os.path.join(remote_branch_path, "Release"))
#         release_control_file = deb822.Release(release_data)
#         archs = release_control_file.get('Architectures').split()
#         comps = release_control_file.get('Components').split()
#         
#         for comp in comps:
#             for arch in archs:
#                 remote_file_path = os.path.join(remote_branch_path, comp, 'binary-' + arch)
#                 local_file_path = os.path.join(local_branch_path, comp, arch)
#                 if not os.path.isdir(local_file_path):
#                     os.makedirs(local_file_path)
#                 control_file = os.path.join(local_file_path, "Packages.gz")
#                 if not os.path.isfile(control_file):
#                     try:
#                         urllib.urlretrieve(remote_file_path, control_file)
#                     # Agregar tipo de excepcion
#                     except:
#                         logger.error('There has been an error trying to get %s' % remote_file_path)
#                 else:
#                     if md5Checksum(control_file) != release_data['md5sum']:
#                         os.remove(control_file)
#                         try:
#                             urllib.urlretrieve(remote_file_path, control_file)
#                         # Agregar tipo de excepcion
#                         except:
#                             logger.error('There has been an error trying to get %s' % remote_file_path)



def create_cache_alt(repository_root, cache_dir_path, debug = True):
    branches = ['aponwao', 'auyantepui', 'roraima', 'kerepakupai', 'kukenan']
    
    for branch in branches:
        remote_branch_path = os.path.join(repository_root, "dists", branch)
        local_branch_path = os.path.join(cache_dir_path, branch)
        
        release_data = urllib.urlopen(os.path.join(remote_branch_path, "Release"))
        release_control_file = deb822.Release(release_data)
        
        archs = release_control_file.get('Architectures').split()
        comps = release_control_file.get('Components').split()
        md5sums = release_control_file.get('MD5Sum')
        
        for comp in comps:
            for arch in archs:
                remote_file_path = os.path.join(remote_branch_path, comp, 'binary-' + arch)
                local_file_path = os.path.join(local_branch_path, comp, arch)
                if not os.path.isdir(local_file_path):
                    os.makedirs(local_file_path)
                remote_control_file_path = os.path.join(remote_file_path, "Packages.gz")
                local_control_file_path = os.path.join(local_file_path, "Packages.gz")
                if not os.path.isfile(local_control_file_path):
                    try:
                        urllib.urlretrieve(remote_control_file_path, local_control_file_path)
                    # Agregar tipo de excepcion
                    except:
                        logger.error('There has been an error trying to get %s' % remote_control_file_path)
                else:
                    for md5sum in md5sums:
                        if md5sum.get('name') == os.path.join(comp, 'binary-' + arch, 'Packages.gz'):
                            if md5Checksum(local_control_file_path) != md5sum.get('md5sum'):
                                os.remove(local_control_file_path)
                                try:
                                    urllib.urlretrieve(remote_control_file_path, local_control_file_path)
                                # Agregar tipo de excepcion
                                except:
                                    logger.error('There has been an error trying to get %s' % remote_control_file_path)
