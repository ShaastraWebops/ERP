from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from erp.tasks.views import *
from erp.users.views import *
from erp.home.views import *
from erp.create_test_data import *
import haystack
from haystack.views import SearchView
from haystack.forms import ModelSearchForm
from haystack.forms import SearchForm
from haystack.views import search_view_factory
haystack.autodiscover()

admin.autodiscover()


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',(r'^createdata/', do_it_all),

    #(r'^search/', include('haystack.urls')),
    url(r'^$', 'erp.home.views.login', name='home'),
    (r'^search/', search_view_factory(
	form_class=ModelSearchForm)),
    #(r'^erp/$', include('erp.home.urls')),
    (r'^erp/home/',include('erp.home.urls')),
    #(r'^erp/users/', include('erp.users.urls')),
    #(r'^erp/dashboard/',include('erp.dashboard.urls')),	
    # Make the above 2 URLConfs look like these 2 below
    (r'^erp/(?P<owner_name>\w+)/users/', include('erp.users.urls')),
    (r'^erp/(?P<owner_name>\w+)/dashboard/',include('erp.dashboard.urls')),	
    (r'^erp/(?P<owner_name>\w+)/', include('erp.tasks.urls')),
    
    (r'^loaddata/$', 'dashboard.views.load_data'),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    
    #(r'^now/sign.html$', sign_in, ),
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

