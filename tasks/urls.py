from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

# TODO
# Caution : Any non-matched url goes straight to display_portal and
# gives an error since a user of that name would not be found.
urlpatterns = patterns('erp.tasks.views',
      (r'^search/', include('haystack.urls')),
      (r'^create', 'edit_task'),
      (r'^edit/([0-9]+)', 'edit_task'),
      (r'^edit/?', 'edit_task'),
      (r'^display_task/([0-9]+)?', 'display_task'),
      (r'^display_subtask/([0-9]+)?', 'display_subtask'),
      (r'^task_comments/([0-9]+)?/', 'handle_task_comments'),
      (r'^subtask_comments/([0-9]+)?/', 'handle_subtask_comments'),
      (r'^department/?(\w+)?$', 'display_department_portal'),
      (r'^(\w+)?$', 'display_portal'),
)

