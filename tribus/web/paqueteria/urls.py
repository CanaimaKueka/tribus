from django.conf.urls import patterns, url
from tribus.web.paqueteria import views

urlpatterns = patterns('',
    url(r'^/index$', views.index, name='index'),
    url(r'^paquetes/$', views.index, name='index'),
    url(r'^paquetes/tags/(?P<tag>(\w*\W*)*)', views.tags, name='tags'),
    url(r'^paquetes/categoria/(?P<categoria>(\w*\W*)*)', views.categoria, name='categoria'),
    url(r'^paquetes/busqueda/(?P<nombre>(\w*\W*)*)', views.urlPaquetes, name='organizador'),    
    )