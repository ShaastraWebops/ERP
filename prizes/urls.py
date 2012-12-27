from django.views.generic.simple import *
from django.contrib import admin
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns = patterns('erp.prizes.views',     
      (r'^assign/$', 'prize_assign'),
      (r'^$', 'prize_details'),
      (r'^testmodelformset/$','testmodelformsetview'),
)

