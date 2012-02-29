from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/$', 'webui.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'webui.views.detail'),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'webui.views.results'),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'webui.views.vote'),
    url(r'^admin/', include(admin.site.urls)),
)
