from django.conf.urls import patterns, url
from tribus.web.profile import views

urlpatterns = patterns('',
	url(r'^profile/$', 'tribus.web.profile.views.UserProfile'),    
    url(r'^settings/$', 'tribus.web.profile.views.EditUserProfile'),
    url(r'^settings/edition$', 'tribus.web.profile.views.EditUserProfile'),
    url(r'^settings/changepassword$', 'tribus.web.profile.views.ChangePassword'),
   )
	