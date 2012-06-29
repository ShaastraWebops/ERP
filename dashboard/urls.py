from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.dashboard.views',
      (r'^contacts/$', 'display_contacts'),
      # (r'^delete_detail/$', 'delete_otherdetails'),
      (r'^upload_document/$', 'upload_file'),
      (r'^delete_document/$', 'delete_file'),
       (r'^delete_document/(?P<number>\w+)$', 'delete_file'),
      (r'^change_profile_pic/$', 'change_profile_pic'),
      (r'^shout/$', 'shout'),
      (r'^display_calendar/$', 'display_calendar'),
      (r'^display_calendar/(?P<month>\w+)/(?P<year>\w+)$', 'display_calendar'),

      (r'^dummy/$', 'test'),
      # (r'^(\w+)?$', 'other_coord'),
)

# Note : home/ URLconf should come before the second one, otherwise
# 'home' itself is considered as a username and so an error results
urlpatterns += patterns('erp.tasks.views',
      (r'^home/?(\w+)?$', 'display_portal'),
      (r'^$', 'display_portal'),
)
	
