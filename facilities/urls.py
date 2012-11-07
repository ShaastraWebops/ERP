from django.views.generic.simple import *
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns=patterns('erp.facilities.views',
    (r'^test/$','test'),
    (r'^create_items/$','create_items'),
    (r'^facilities_home/$','facilities_home'),
    (r'^add_round/$','add_round'),
    (r'^portal/(?P<roundno>\d+)/$','portal'),
    (r'^display/(?P<roundno>\d+)/$','display'),    
    (r'^approval_portal/$','approval_portal'),
    (r'^qms_visible_portal/$','qms_visible_portal'),
    (r'^approve_event/(?P<event_name>\d+)/(?P<form_saved>\d+)/(?P<error>\d+)/$','approve_event'),
    (r'^submit_approval/(?P<item_id>\d+)/$','submit_approval'),
    (r'^overallpdf/$', 'generateOverallPDF'),
    (r'^eventpdf/(?P<event_id>\d+)/$', 'generateEventPDF'),
)
        