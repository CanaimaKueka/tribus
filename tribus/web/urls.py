#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from tastypie.api import Api
from tribus.web.api.resources import TribResource, UserResource

api_01 = Api(api_name='0.1')
api_01.register(TribResource())
api_01.register(UserResource())

urlpatterns = patterns(
    '',

    url(r'^$', 'tribus.web.views.index'),
    url(r'^tour/$', 'tribus.web.views.tour'),

    url(r'', include('tribus.web.user.urls')),
    url(r'', include('tribus.web.paqueteria.urls')),
    url(r'', include('tribus.web.profile.urls')),
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

    url(r'^api/', include(api_01.urls)),

    url(r'^admin/', include(admin.site.urls)),
)
