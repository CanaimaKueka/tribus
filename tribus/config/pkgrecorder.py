#===============================================================================
# CONSTANTES UTILIZADAS POR EL MODULO DE REGISTRO DE PAQUETES
#===============================================================================

import os
from tribus.config.base import BASEDIR
# Modificar ubicacion del repositorio y agregar a gitignore
LOCAL_ROOT = "http://localhost/repositorio"
LOCAL_ROOT_DISTS = os.path.join(LOCAL_ROOT, 'dists')
CANAIMA_ROOT = "http://paquetes.canaima.softwarelibre.gob.ve"
SAMPLES = os.path.join(BASEDIR, 'package_samples')
SAMPLES_LISTS = os.path.join(SAMPLES, 'lists')
SAMPLES_PACKAGES = os.path.join(SAMPLES, 'packages')

package_fields = ["Package", "Description", "Homepage", "Section", 
                  "Priority", "Essential", "Bugs", "Multi-Arch"] 
detail_fields = ["Version", "Architecture", "Size", "MD5sum", "Filename",
                 "Installed-Size"]
relation_types = ["pre-depends", "depends", "recommends", "suggests",
                  "provides", "enhances", "breaks", "replaces", "conflicts"]
