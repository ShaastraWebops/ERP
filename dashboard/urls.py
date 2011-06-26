from django.conf.urls.defaults import *
from django.views.generic.simple import *
from django.contrib import admin

urlpatterns = patterns('erp.dashboard.views',
      (r'^documents/$', 'details'),
      (r'^delete_detail/$', 'delete_otherdetails'),
      (r'^upload_document/$', 'upload_file'),
      (r'^delete_document/$', 'delete_file'),
      (r'^change_profile_pic/$', 'change_profile_pic'),
      (r'^shout/$', 'shout'),
)


urlpatterns += patterns('erp.tasks.views',
      (r'^$', 'display_portal'),
      (r'^home/$', 'display_portal'),
)
	
