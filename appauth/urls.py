from django.conf.urls import patterns, url

from appauth import views


urlpatterns = [

	url(r'^signin/$',
		views.signin,
		name='signin'
	),

	url(r'^logout/$',
		views.signout,
		name='signout'
	),
	
	url(r'^users/profile/(?P<user_id>[a-zA-Z0-9-]+)/$',
		views.user_profile,
		name='user_profile'
	)
]
