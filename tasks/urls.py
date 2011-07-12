from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

# TODO
# Caution : Any non-matched url goes straight to display_portal and
# gives an error since a user of that name would not be found.
urlpatterns = patterns('erp.tasks.views',
      (r'^$', 'display_portal'),
      (r'^search/', include('haystack.urls')),
      (r'^create', 'edit_task'),
      (r'^edit/(?P<task_id>[0-9]+)', 'edit_task'),
      (r'^edit/?', 'edit_task'),
      (r'^display_task/(?P<task_id>[0-9]+)?', 'display_task'),
      (r'^display_subtask/(?P<subtask_id>[0-9]+)?', 'display_subtask'),
      (r'^task_comments/(?P<task_id>[0-9]+)?/', 'handle_task_comments'),
      (r'^subtask_comments/(?P<subtask_id>[0-9]+)?/', 'handle_subtask_comments'),
      (r'^department/(?P<department_name>$\w+)?$', 'display_department_portal'),
      # (r'^(\w+)?$', 'display_portal'),
)

