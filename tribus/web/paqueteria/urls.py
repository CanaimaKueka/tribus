from django.conf.urls import patterns, url
#from paqueteria import views
from tribus.web.paqueteria import views

urlpatterns = patterns('',
    url(r'^paqueteria/$', views.inicio, name='inicio'),
    url(r'^/index$', views.index, name='index'),
    url(r'^paqueteria/tags/(?P<tag>(\w*\W*)*)', views.tags, name='tags'),    
    url(r'^paqueteria/busqueda/info/(?P<args>(\w*\W*)*)', views.info, name='busqueda'),
    url(r'^paqueteria/busqueda/(?P<pqt>(\w*\W*)*)', views.busqueda, name='info'),
    url(r'^paqueteria/categoria/(?P<categoria>(\w*\W*)*)', views.categoria, name='categoria'),

    )
