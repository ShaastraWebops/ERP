from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.tasks.views',
      (r'^$', 'display_portal'),
      (r'^create/', 'create_task'),
      (r'^edit/([0-9]+)?', 'edit_task'),
      (r'^display_task/([0-9]+)?', 'display_task'),
      (r'^display_subtask/([0-9]+)?', 'display_subtask'),
      (r'^task_comments/([0-9]+)?/', 'handle_task_comments'),
      (r'^subtask_comments/([0-9]+)?/', 'handle_subtask_comments'),
)

