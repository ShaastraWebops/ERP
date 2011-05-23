from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.tasks.views',
      (r'^create/$', 'create_task'),
)

