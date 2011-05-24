from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.tasks.views',
      (r'^create/$', 'create_task'),
      (r'^timeline/$', 'timeline'),
      (r'^core_portal/$', 'core_portal'),
      (r'^core_portal/listoftasks/', 'listoftasks'),
      (r'^core_portal/completed_subtasks/', 'completedsubtasks'),
)

