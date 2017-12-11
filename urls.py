from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('extempore.views',
	
	url(r'^(?P<num>.+)$', 'funpage', name='extempore_fun_detail'),
	
	url(r'^$', 'index', name='extempore_home'),
	
)

