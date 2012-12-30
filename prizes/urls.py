from django.views.generic.simple import *
from django.contrib import admin
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns = patterns('erp.prizes.views',     
      (r'^prize/$', 'prize_assign'),
      (r'^$', 'cheque_assign'),
      (r'^registerparticipants/$','registerparticipants'),
      (r'^assign/$','assign_barcode'),  
)

