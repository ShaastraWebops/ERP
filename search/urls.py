from erp.search.views import *
from django.conf.urls import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', search),
    (r'^(?P<search_term>[^/]+)/$', search),
    )
