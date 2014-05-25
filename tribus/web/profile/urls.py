from django.conf.urls import patterns, url
from django.contrib.auth.views import *

urlpatterns = patterns('',

                       url(r'^profile/done/$',
                           view='tribus.web.profile.views.UserProfile',
                           name='userprofile1',
                           ),

                       url(r'^profile/(?P<nick>(\w*\W*)*)/$',
                           view='tribus.web.profile.views.SearchProfile',
                           name='SearchProfile',
                           ),

                       url(r'^profile/$',
                           view='tribus.web.profile.views.UserProfile',
                           name='userprofile2',
                           ),
                       )
