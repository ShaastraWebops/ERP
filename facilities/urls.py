from django.views.generic.simple import *
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns=patterns('erp.facilities.views',
    (r'^test/$','test'),
    (r'^portal/$','portal'),
    (r'^display/$','display'),    
    (r'^approval_portal/$','approval_portal'),
    (r'^approve_event/(?P<event_name>\d+)/(?P<form_saved>\d+)/(?P<error>\d+)/$','approve_event'),
    (r'^submit_approval/(?P<item_id>\d+)/$','submit_approval'),
)
        
