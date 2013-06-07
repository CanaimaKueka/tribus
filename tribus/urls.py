#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from tribus.core.views import Init, Login, Logout, Dashboard, Tour

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Init),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^i/$', Dashboard),
    url(r'^tour/$', Tour),
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
#    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^skins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
    )
