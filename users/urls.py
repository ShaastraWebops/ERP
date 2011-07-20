from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.users.views',
      (r'^$', 'handle_profile'),
      (r'^register/?(?P<dept_name>\w+)?/$', 'register_user'),
      # (r'^register_invite/?(\w+)?/?(\w+)?/?(\w+)?/$', 'register_invite'),
      (r'^invite/$', 'invite'),
      (r'^profile/$', 'view_profile'),
      (r'^edit_profile/$', 'handle_profile'),
      (r'^search/', include('haystack.urls')),

)

urlpatterns +=patterns('',
      (r'^change_profile_pic/$', 'erp.dashboard.views.change_profile_pic'),
)
