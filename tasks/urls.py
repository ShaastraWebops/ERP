from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.tasks.views',
      (r'^create/', 'create_task'),
      (r'^edit/([0-9]+)?', 'edit_task'),
      (r'^display/([0-9]+)?', 'display_subtask'),
      # (r'^portal/$', 'display_portal'),
      (r'^core_portal/$', 'core_portal'),
      (r'^core_portal/listoftasks/', 'listoftasks'),
      (r'^core_portal/completed_subtasks/', 'completedsubtasks'),
      (r'^task_comments/([0-9]+)?/', 'task_comment'),
      (r'^sub_task_comments/([0-9]+)?/', 'sub_task_comment'),

)

