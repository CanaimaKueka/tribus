import os
import urllib
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
from debian import deb822
from tribus.web.cloud.models import Package, Details
from tribus.common.utils import readconfig

canaima = 'http://paquetes.canaima.softwarelibre.gob.ve'
selected = '/home/fran/workspace/tribus/selected_samples'

lista = readconfig(os.path.join(selected, 'lista.txt'), None, False, False)

with open("/home/tribus/lista.txt", "w") as f:
    for d in Details.objects.filter(Size__lt = 2000):
        p = Package.objects.get(Details = d)
        f.write("%s %s %s \n" %  (p.Package, d.Distribution, d.Filename))
        
         
