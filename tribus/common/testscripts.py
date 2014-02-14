import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

from tribus.common.recorder import record_maintainer
from tribus.web.cloud.models import Maintainer

mantenedores = [
"Jose Simon Antonio de la Santisima Trinidad Bolivar Palacios y Blanco <josesimonantoniodelasantisimatrinidadbolivarypalaciosblanco@josesimonantoniodelasantisimatrinidadbolivarypalaciosblanco.com",
"mm <mm@mmngmnt.com>",
"Jose Francisco Guerrero Rangel <jsfrncscg@gmail.com>"
]

for man in mantenedores:
    record_maintainer(man)
    
print Maintainer.objects.all()