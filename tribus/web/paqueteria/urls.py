from django.conf.urls import patterns, url
#from paqueteria import views
from tribus.web.paqueteria import views

urlpatterns = patterns('',
    #url(r'^paquetes/$', views.busquedaForm, name='buscar'),
    url(r'^paquetes/$', views.index, name='index'),
    url(r'^/index$', views.index, name='index'),
    url(r'^paquetes/tags/(?P<tag>(\w*\W*)*)', views.tags, name='tags'),
    url(r'^paquetes/busqueda/arq/(?P<pqt>(\w*\W*)*)', views.organizador, name='organizador'),
    url(r'^paquetes/busqueda/pqt/(?P<pqt>(\w*\W*)*)', views.detallador, name='detallador'),
    url(r'^paquetes/busqueda/', views.buscar, name='organizador'),
    url(r'^paquetes/categoria/(?P<categoria>(\w*\W*)*)', views.categoria, name='categoria'),

    )
