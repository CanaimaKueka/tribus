#===============================================================================
# CONSTANTES UTILIZADAS POR EL MODULO DE REGISTRO DE PAQUETES
#===============================================================================

import os
from tribus.config.base import BASEDIR
LOCAL_ROOT = os.path.join("file://", BASEDIR, "test_repo")
CANAIMA_ROOT = "http://paquetes.canaima.softwarelibre.gob.ve"
SAMPLES = os.path.join(BASEDIR, 'package_samples')

package_fields = ["Package", "Description", "Homepage", "Section", 
                  "Priority", "Essential", "Bugs", "Multi-Arch"] 
detail_fields = ["Version", "Architecture", "Size", "MD5sum", "Filename",
                 "Installed-Size"]
relation_types = ["pre-depends", "depends", "recommends", "suggests",
                  "provides", "enhances", "breaks", "replaces", "conflicts"]

codenames = {'aponwao' : '2.1', 'roraima' : '3.0', 'auyantepui' : '3.1',
             'kerepakupai' : '4.0', 'kukenan' : '4.1'}
