from django.views.generic.simple import *
from django.contrib import admin
from django.conf.urls import *

# TODO
# Caution : Any non-matched url goes straight to display_portal and
# gives an error since a user of that name would not be found.
urlpatterns = patterns('erp.tasks.views',
      (r'^$', 'display_portal'),
      #(r'^search/', include('haystack.urls')),

      (r'^create', 'edit_task'),
      (r'^task/(?P<task_id>[0-9]+)', 'edit_task'),
      (r'^display_task/(?P<task_id>[0-9]+)?', 'display_task'),
      (r'^subtask/(?P<subtask_id>[0-9]+)', 'edit_subtask'),
      (r'^display_subtask/(?P<subtask_id>[0-9]+)?', 'display_subtask'),
      (r'^department/(?P<department_name>$\w+)?$', 'display_department_portal'),
      # (r'^(\w+)?$', 'display_portal'),
)

urlpatterns +=patterns('erp.tasks.pdfMakeViews',
      (r'^report/$', 'ReportGen'),
)

