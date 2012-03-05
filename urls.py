#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', 'viewer.views.welcome'),
    url(r'^welcome/$', 'viewer.views.welcome'),
    url(r'^login/$', 'viewer.views.login'),
    url(r'^signup/$', 'viewer.views.signup'),
    url(r'^preferences/$', 'viewer.views.preferences'),
    url(r'^distro/$', 'viewer.views.distro'),
    url(r'^distro/(?P<distroname>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.distro'),
    url(r'^doc/$', 'viewer.views.doc'),
    url(r'^doc/(?P<docname>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.doc'),
    url(r'^team/$', 'viewer.views.team'),
    url(r'^team/(?P<teamname>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.team'),
    url(r'^event/$', 'viewer.views.event'),
    url(r'^event/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.event'),
    url(r'^user/$', 'viewer.views.user'),
    url(r'^user/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.user'),
    url(r'^pkg/$', 'viewer.views.pkg'),
    url(r'^pkg/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'viewer.views.pkg'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
    )
