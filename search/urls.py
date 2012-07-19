from erp.search.views import *
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^$', search),
    (r'^(?P<search_term>[^/]+)/$', search),
    )
