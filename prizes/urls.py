from django.views.generic.simple import *
from django.contrib import admin
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns = patterns('erp.prizes.views',     
      (r'^assign_new/$','assign_barcode_new'),
      (r'^upload/$', 'upload_file'),
      (r'^upload/(?P<event_name>\d{1,3})/$', 'upload_file'),
      (r'^eventdetails/$','fillEventDetails'),
      (r'^eventdetails/(?P<event_name>\d{1,3})/$','fillEventDetails'),      
      (r'^prize/$', 'choosePosition'),
      (r'^prize/(?P<event_name>\d{1,3})/$', 'choosePosition'),
      (r'^prize/(?P<event_name>\d{1,3})/position/$', 'prize_assign'),
      (r'^prize/(?P<event_name>\d{1,3})/position/(?P<position>\d{1,2})/$', 'prize_assign'),
      #(r'^cheque/$', 'cheque_assign'),
      #(r'^cheque/(?P<event_name>\d{1,3})/$', 'cheque_assign'),
      (r'^registerparticipants/$','registerparticipants'),
      (r'^registerparticipants/(?P<event_name>\d{1,3})/$','registerparticipants'),
      (r'^assign/$','assign_barcode'),  
)


