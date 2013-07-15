#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
# from django.conf import settings

admin.autodiscover()

from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',

    url(r'^$', 'tribus.web.views.index'),
    url(r'^tour/$', 'tribus.web.views.tour'),

    url(r'', include('tribus.web.user.urls')),
    url(r'', include('social_auth.urls')),


#   url('^page/(?P<page>\\d+)/$', 'index'),
#   url('^register/$', 'register'),
#   url('^configuracion/$', 'conf'),
#   
#   url('^profile/(?P<username>[a-zA-Z0-9\\_]+)/$', 'profile'),
#   url('^profile/(?P<username>[a-zA-Z0-9\\_]+)/page/(?P<page>\\d+)/$', 'profile'),
#   
#   url('^tweet/$', 'tweet'),
#   url('^follow/$', 'follow'),
#   url('^retweet/(?P<tweet_id>\\d+)/$', 'retweet'),
#   url('^borrar/(?P<tweet_id>\\d+)/$', 'borrar'),
#   url('^responder/(?P<tweet_id>\\d+)/$', 'responder'),

#   url('^conversacion/(?P<conversacion>\\d+)/$', 'conversacion'),
#   url('^conversacion/(?P<conversacion>\\d+)/page/(?P<page>\\d+)/$', 'conversacion'),

#   url('^buscar/$', 'buscar'),
#   url('^buscar/page/(?P<page>\\d+)/$', 'buscar'),
#   
#   url('^(?P<method>(seguidores|siguiendo))/(?P<username>[a-zA-Z0-9\\_]+)/$', 'seguidores'),

#   url('^chat/$', 'chat'),
#   url('^newtweets/$', 'ajaxtw'),
#    url(r'^m/$', include(tribus.postman.urls)),
#    url(r'^u/$', include(tribus.profiles.urls)),
#    url(r'^signup/$', 'tribus.viewer.views.signup'),
#    url(r'^preferences/$', 'tribus.viewer.views.preferences'),
#    url(r'^distro/$', 'tribus.viewer.views.distro'),
#    url(r'^distro/(?P<distroname>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.distro'),
#    url(r'^doc/$', 'tribus.viewer.views.doc'),
#    url(r'^doc/(?P<docname>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.doc'),
#    url(r'^team/$', 'tribus.viewer.views.team'),
#    url(r'^team/(?P<teamname>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.team'),
#    url(r'^event/$', 'tribus.viewer.views.event'),
#    url(r'^event/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.event'),
#    url(r'^user/$', 'tribus.viewer.views.user'),
#    url(r'^user/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.user'),
#    url(r'^pkg/$', 'tribus.viewer.views.pkg'),
#    url(r'^pkg/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'tribus.viewer.views.pkg'),
    url(r'^admin/', include(admin.site.urls)),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
#     )
