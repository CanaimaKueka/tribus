#===============================================================================
# CONSTANTES UTILIZADAS POR EL MODULO DE REGISTRO DE PAQUETES
#===============================================================================

raiz = "http://localhost/repositorio/"
local = "http://localhost/repositorio/dists/"

i386  = "http://10.16.106.152/repositorio/dists/waraira/main/binary-i386/Packages"
amd64 = "http://10.16.106.152/repositorio/dists/waraira/main/binary-amd64/Packages"

canaimai386 = "http://paquetes.canaima.softwarelibre.gob.ve/dists/kerepakupai/main/binary-i386/Packages"
canaimaamd64 = "http://paquetes.canaima.softwarelibre.gob.ve/dists/kerepakupai/main/binary-amd64/Packages"

package_fields = ["Package", "Description", "Homepage", "Section", 
                  "Priority", "Essential", "Bugs", "Multi-Arch"] 
detail_fields = ["Version", "Architecture", "Size", "MD5sum", "Filename",
                 "Installed-Size"]
relation_types = ["pre-depends", "depends", "recommends", "suggests",
                  "provides", "enhances", "breaks", "replaces", "conflicts"]
