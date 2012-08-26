from erp.search.views import *
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$', search),
    (r'^(?P<search_term>[^/]+)/$', search),
    )
