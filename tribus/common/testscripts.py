import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from tribus.web.cloud.models import Package, Details
from debian import deb822

# mantenedores = [
# "Jose Simon Antonio de la Santisima Trinidad Bolivar Palacios y Blanco <josesimonantoniodelasantisimatrinidadbolivarypalaciosblanco@josesimonantoniodelasantisimatrinidadbolivarypalaciosblanco.com",
# "mm <mm@mmngmnt.com>",
# "Jose Francisco Guerrero Rangel <jsfrncscg@gmail.com>"
# ]
# 
# for man in mantenedores:
#     record_maintainer(man)
#     
# print Maintainer.objects.all()

x = deb822.Packages(open("/home/fran/Escritorio/Package"))

p = Package.objects.create(x)
print p.Labels.all()

d = Details.objects.create(x, p, 'kukenan')
d.record_relations(x.relations.items())

print d.Relations.all()