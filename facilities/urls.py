from django.views.generic.simple import *
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns=patterns('erp.facilities.views',
    (r'^test/$','test'),
    (r'^create_items/$','create_items'),
    (r'^create_rounds/$','create_rounds'),
    (r'^facilities_home/$','facilities_home'),
    (r'^portal/(?P<roundno>\d+)/$','portal'),
    (r'^display/(?P<roundno>\d+)/$','display'),    
    (r'^approval_portal/$','approval_portal'),
    (r'^qms_visible_portal/$','qms_visible_portal'),
    (r'^eventpdf/(?P<event_id>\d+)/$', 'generateEventPDF'),
    (r'^round_home/(?P<event_id>\d+)/$','round_home'),   
    (r'^add_round/(?P<event_id>\d+)/$','add_round'),
    (r'^delete_round/(?P<round_id>\d+)/$','delete_round'),
    (r'^approve_event/(?P<round_id>\d+)/(?P<form_saved>\d+)/(?P<error>\d+)/$','approve_event'),
    (r'^submit_approval/(?P<item_id>\d+)/$','submit_approval'),
    (r'^submit_round/(?P<round_id>\d+)/$','submit_round'),
    
    
)
urlpatterns+=patterns('',
    (r'^overallpdf/$', 'erp.facilities.pdfGeneratingViews.generateOverallPDF'),
    (r'^test_excel/$', 'erp.facilities.excelViews.test_excel'),
    (r'^generate_round_excel/(?P<round_id>\d+)/$', 'erp.facilities.excelViews.generate_round_excel'),
)
        
