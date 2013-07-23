from django.conf.urls import patterns, url
#from paqueteria import views
from tribus.web.paqueteria import views

urlpatterns = patterns('',
    url(r'^$', views.inicio, name='inicio'),
    url(r'^/index$', views.index, name='index'),
    #url(r'^(?P<pqt>\w*-?\w*)', views.busqueda, name='busqueda'),
    #url(r'^(?P<pqt>\w*\.*?-*\w*)', views.busqueda, name='busqueda'),
    #url(r'^(?P<pqt>(\w*-?\w*:-*?\w*)', views.busqueda, name='busqueda'),
    url(r'^tags/(?P<tag>(\w*\W*)*)', views.tags, name='tags'),    
    url(r'^busqueda/(?P<pqt>(\w*\W*)*)', views.busqueda, name='busqueda'),
    url(r'^categoria/(?P<categoria>(\w*\W*)*)', views.categoria, name='categoria'),
    )
