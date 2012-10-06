from django.views.generic.simple import *
from django.conf.urls import *
from django.conf.urls.defaults import *


urlpatterns=patterns('erp.finance.views',
    (r'^display/(?P<event_name>\d+)/$','display'),
    (r'^toggle/$','toggle'),
    (r'^submit/(?P<event>\d+)/$','submit'),
    (r'^perms/$','permissions'),
	(r'^(?P<plan>\w+)/$','budget_portal'),

)
