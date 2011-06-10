from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('',
      (r'^$', 'erp.tasks.views.display_portal'),
      (r'^home/$', 'erp.tasks.views.display_portal'),
      (r'^documents/$', 'erp.dashboard.views.documents'),
      (r'^addteammember/$', 'erp.dashboard.views.addteammember'),
      (r'^upload_document/$', 'erp.dashboard.views.upload_file'),
)

