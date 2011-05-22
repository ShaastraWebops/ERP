from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('dashboard.views',
      (r'^home/$', 'home'),

)

