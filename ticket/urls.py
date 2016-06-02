from django.conf.urls import patterns, url

from ticket import views

urlpatterns = [

	url(r'^$',
		views.index,
		name='tickets_index'
	),

	url(r'^resolved$',
		views.resolved,
		name='tickets_resolved'
	),

	url(r'^canceled$',
		views.canceled,
		name='tickets_canceled'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/$',
		views.view,
		name='tickets_view'
	),

	url(r'^add/$',
		views.add,
		name='tickets_add'
	),

	url(r'^upload/$',
		views.upload,
		name='tickets_upload'
	),

	url(r'^download/(?P<hash>[a-zA-Z0-9-]+)/$',
		views.download,
		name='tickets_download'
	),

	url(r'^edit/(?P<ticket_slug>[a-zA-Z0-9-]+)/',
		views.edit,
		name='tickets_edit'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/action/assign-to',
		views.assign_to,
		name='tickets_assign_to'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/action/cancel',
		views.cancel,
		name='tickets_cancel'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/action/re-open',
		views.re_open,
		name='tickets_re_open'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/action/solve',
		views.solve,
		name='tickets_solve'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/comment',
		views.comment,
		name='tickets_comment'
	),

	url(r'^view/(?P<ticket_slug>[a-zA-Z0-9-]+)/delete-comment/(?P<comment_id>[a-zA-Z0-9-]+)',
		views.delete_comment,
		name='tickets_delete_comment'
	)
]
