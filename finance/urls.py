from django.views.generic.simple import *
from django.conf.urls import *


urlpatterns=patterns('erp.finance.views',
	(r'^$','budget_portal'),

)
