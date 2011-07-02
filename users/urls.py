from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.users.views',
      (r'^$', 'handle_profile'),
      (r'^register/$', 'register_user'),
      (r'^register_invite/?(\w+)?/?(\w+)?/?(\w+)?/$', 'register_invite'),
      (r'^invite/$', 'invite'),
      (r'^profile/$', 'handle_profile'),
      #(r'^search/', include('haystack.urls')),
)
#      (r'^department/?(\w+)?$', 'display_department_portal'),
