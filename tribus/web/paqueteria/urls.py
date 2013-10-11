from django.conf.urls import patterns, url
from tribus.web.paqueteria import views

urlpatterns = patterns('',
    url(r'^/index$', views.index, name='index'),
    url(r'^packages/$', views.index, name='index'),
    url(r'^packages/tags/(?P<tag>(\w*\W*)*)', views.viewtags, name='tags'),
    url(r'^packages/category/(?P<category>(\w*\W*)*)', views.viewcategory, name='category'),
    url(r'^packages/search/(?P<name>(\w*\W*)*)', views.viewpackages, name='organizer'),
    )
