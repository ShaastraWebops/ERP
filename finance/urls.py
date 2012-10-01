from django.views.generic.simple import *
from django.conf.urls import *


urlpatterns=patterns('erp.finance.views',
    (r'^display/(?P<event_name>\w+)/$','display'),
    (r'^toggle/$','toggle'),
    (r'^submit/(?P<event>\w+)/$','submit'),
    (r'^perms/$','permissions'),
	(r'^(?P<plan>\w+)/$','budget_portal'),

)
