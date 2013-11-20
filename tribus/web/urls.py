#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from tribus.web.api import api_01

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'tribus.web.views.index'),
    url(r'^tour/$', 'tribus.web.views.tour'),
    url(r'^search/$', 'tribus.web.views.tribus_search'),
    url(r'', include('tribus.web.registration.urls')),
    url(r'', include('tribus.web.cloud.urls')),
    url(r'', include('tribus.web.profile.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^api/', include(api_01.urls)),
    url(r'^admin/', include(admin.site.urls)),
)