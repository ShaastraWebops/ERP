from django.views.generic.simple import *
from django.conf.urls import *


urlpatterns=patterns('erp.finance.views',
    (r'^display/$','display'),
    (r'^toggle/$','toggle'),
    (r'^perms/$','permissions'),
	(r'^(?P<plan>\w+)/$','budget_portal'),

)
