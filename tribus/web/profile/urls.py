from django.conf.urls import patterns, url
from django.contrib.auth.views import *
#from tribus.web.profile import views

urlpatterns = patterns('',

    url(r'^profile/done$', 
        view='tribus.web.profile.views.UserProfile'
        ),

    url(r'^profile/(?P<nick>(\w*\W*)*)', 
        view='tribus.web.profile.views.SearchProfile'
        ),

	url(r'^profile$', 
        view='tribus.web.profile.views.UserProfile'
        ),
    )
