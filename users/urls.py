from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.users.views',
      (r'^$', 'register_user'),
      (r'^register/$', 'register_user'),
      (r'^invite_page/$', 'invite_page'),
      (r'^invite/$', 'invite'),
      (r'^contact_details/$', 'contact_details'),

)

