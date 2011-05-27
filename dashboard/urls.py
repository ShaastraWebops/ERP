from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('',
      (r'^$', 'erp.tasks.views.display_portal'),
      (r'^home/$', 'erp.tasks.views.display_portal'),

)

