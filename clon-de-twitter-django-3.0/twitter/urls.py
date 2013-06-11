from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('twitter.views',
	url('^$', 'index'),
	url('^page/(?P<page>\\d+)/$', 'index'),

	url('^login/$', 'twitter_login'),
	url('^login/process/$', 'login_process'),
	url('^logout/$', 'twitter_logout'),
	url('^register/$', 'register'),
	url('^configuracion/$', 'conf'),
	
	url('^profile/(?P<username>[a-zA-Z0-9\\_]+)/$', 'profile'),
	url('^profile/(?P<username>[a-zA-Z0-9\\_]+)/page/(?P<page>\\d+)/$', 'profile'),
	
	url('^tweet/$', 'tweet'),
	url('^follow/$', 'follow'),
	url('^retweet/(?P<tweet_id>\\d+)/$', 'retweet'),
	url('^borrar/(?P<tweet_id>\\d+)/$', 'borrar'),
	url('^responder/(?P<tweet_id>\\d+)/$', 'responder'),

	url('^conversacion/(?P<conversacion>\\d+)/$', 'conversacion'),
	url('^conversacion/(?P<conversacion>\\d+)/page/(?P<page>\\d+)/$', 'conversacion'),

	url('^buscar/$', 'buscar'),
	url('^buscar/page/(?P<page>\\d+)/$', 'buscar'),
	
	url('^(?P<method>(seguidores|siguiendo))/(?P<username>[a-zA-Z0-9\\_]+)/$', 'seguidores'),

	url('^chat/$', 'chat'),
	url('^newtweets/$', 'ajaxtw'),
)
