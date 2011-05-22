from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from erp.tasks.views import *
from erp.users.views import *
from erp.home.views import *
admin.autodiscover()


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^erp/users/', include('erp.users.urls')),
    (r'^erp/home/',include('erp.home.urls')),
    (r'^erp/dashboard/',include('erp.dashboard.urls')),	
    #(r'^now/sign.html$', sign_in, ),
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

