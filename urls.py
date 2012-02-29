from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', redirect_to, {'url': '/welcome/'}),
    url(r'^welcome/$', 'webui.views.welcome'),
    url(r'^login/$', 'webui.views.login'),
    url(r'^signup/$', 'webui.views.signup'),
    url(r'^distro/$', 'webui.views.distro'),
    url(r'^distro/(?P<distroname>[a-zA-Z0-9_.-]*)/*$', 'webui.views.distro'),
    url(r'^doc/$', 'webui.views.docs'),
    url(r'^doc/(?P<docname>[a-zA-Z0-9_.-]*)/*$', 'webui.views.doc'),
    url(r'^team/$', 'webui.views.team'),
    url(r'^team/(?P<teamname>[a-zA-Z0-9_.-]*)/*$', 'webui.views.team'),
    url(r'^event/$', 'webui.views.event'),
    url(r'^event/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'webui.views.event'),
    url(r'^user/$', 'webui.views.user'),
    url(r'^user/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'webui.views.user'),
    url(r'^pkg/$', 'webui.views.pkg'),
    url(r'^pkg/(?P<action>[a-zA-Z0-9_.-]*)/(?P<term>[a-zA-Z0-9_.-]*)/*$', 'webui.views.pkg'),
    url(r'^admin/', include(admin.site.urls)),
)
