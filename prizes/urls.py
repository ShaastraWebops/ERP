from django.views.generic.simple import *
from django.contrib import admin
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns = patterns('erp.prizes.views',     
      (r'^prize/$', 'prize_assign'),
      (r'^cheque/$', 'cheque_assign'),
      (r'^cheque/(?P<event_name>\d{1,3})/$', 'cheque_assign'),
      (r'^eventdetails/$','fillEventDetails'),
      (r'^eventdetails/(?P<event_name>\d{1,3})/$','fillEventDetails'),      
      (r'^registerparticipants/$','registerparticipants'),
      (r'^registerparticipants/(?P<event_name>\d{1,3})/$','registerparticipants'),
      (r'^assign/$','assign_barcode'),  
)


