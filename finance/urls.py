from django.views.generic.simple import *
from django.conf.urls import *


urlpatterns=patterns('erp.finance.views',
    (r'^display/(?P<event_name>\w+)/$','display'),
	(r'^(?P<plan>\w+)/$','budget_portal'),
	
)
