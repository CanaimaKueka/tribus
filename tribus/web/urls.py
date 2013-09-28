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
    url(r'^profile/$', 'tribus.web.views.UserProfile'),
    url(r'^tour/$', 'tribus.web.views.tour'),
    url(r'^settings/$', 'tribus.web.views.EditUserProfile'),
    url(r'^settings/edition$', 'tribus.web.views.EditUserProfile'),
    url(r'^settings/changepassword$', 'tribus.web.views.ChangePassword'),


    url(r'', include('tribus.web.user.urls')),
    url(r'', include('tribus.web.paqueteria.urls')),
    url(r'', include('social_auth.urls')),


    url(r'^api/', include(api_01.urls)),

    url(r'^admin/', include(admin.site.urls)),
)
