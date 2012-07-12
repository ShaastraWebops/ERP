from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('erp.home.views',
      #(r'^$', 'login'),
      #(r'^login/$', 'login'),
      (r'^forgot_password/$', 'forgot_password'),
      #(r'^login/forgot/$', 'forgot_password'),
      #(r'^login/forgot/(?P<u_name>[a-zA-Z0-9_.-]+)/(?P<new_pass>[\w]+)/?$', 'reset_password'),
      (r'^logout/$', 'logout'),
      #(r'^check/$','check'),
      #(r'^deadlines/$','deadlines'),
      #(r'^registered/$','registered'),
)

