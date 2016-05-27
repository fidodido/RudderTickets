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
	)
]
