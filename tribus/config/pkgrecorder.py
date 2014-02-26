#=========================================================================
# CONSTANTES UTILIZADAS POR EL MODULO DE REGISTRO DE PAQUETES
#=========================================================================

import os
from tribus.config.base import BASEDIR
LOCAL_ROOT = os.path.join("file://", BASEDIR, "test_repo")
CANAIMA_ROOT = "http://paquetes.canaima.softwarelibre.gob.ve"
SAMPLES_DIR = os.path.join(BASEDIR, 'package_samples')

PACKAGE_FIELDS = {'Package':'Name', 'Description':'Description',
                  'Homepage':'Homepage', 'Section':'Section',
                  'Priority':'Priority', 'Essential':'Essential',
                  'Bugs':'Bugs', 'Multi-Arch':'MultiArch'}

DETAIL_FIELDS = {'Version':'Version', 'Architecture':'Architecture',
                 'Size':'Size', 'MD5sum':'MD5sum', 'Filename':'Filename',
                 'Installed-Size':'InstalledSize'}

relation_types = ["pre-depends", "depends", "recommends", "suggests",
                  "provides", "enhances", "breaks", "replaces", "conflicts"]

codenames = {'aponwao': '2.1', 'roraima': '3.0', 'auyantepui': '3.1',
             'kerepakupai': '4.0', 'kukenan': '4.1'}
