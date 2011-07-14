from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.dashboard.views',
      (r'^contacts/$', 'display_contacts'),
      # (r'^delete_detail/$', 'delete_otherdetails'),
      (r'^upload_document/(\w+)?$', 'upload_file'),
      (r'^delete_document/$', 'delete_file'),
      # (r'^delete_document/(?P<owner_name>\w+)/(?P<number>\w+)/(?P<file_name>\w+)$', 'delete_file'),
      (r'^change_profile_pic/$', 'change_profile_pic'),
      (r'^shout/$', 'shout'),
      (r'^dummy/$', 'test'),
      # (r'^(\w+)?$', 'other_coord'),
)

# Note : home/ URLconf should come before the second one, otherwise
# 'home' itself is considered as a username and so an error results
urlpatterns += patterns('erp.tasks.views',
      (r'^home/?(\w+)?$', 'display_portal'),
      (r'^(\w+)?$', 'display_portal'),
)
	
