from django.conf.urls import *
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover
from django.conf import settings
from erp.tasks.views import *
from erp.users.views import *
from erp.home.views import *
from erp.feedback.views import *
from erp.finance.views import *
import haystack
from haystack.views import SearchView
from haystack.forms import ModelSearchForm
from haystack.forms import SearchForm
from haystack.views import search_view_factory
from django.conf.urls import *
from tasks.views import *
from django.conf.urls.defaults import *

#haystack.autodiscover()
#dajaxice_autodiscover()
#admin.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
 
urlpatterns = patterns('',
    #(r'^134c036048b637ac75edcd4352212e55/$', 'erp.home.dbscript.write_into_db'), #used to load coord/core details into db.
    (r'^dajaxice/', include('dajaxice.urls')),
    url(r'^account/', include('django.contrib.auth.urls')),
    (r'^forgot_password/$','erp.home.views.forgot_password'),
    #(r'^search/', include('haystack.urls')),
    url(r'^$', 'erp.home.views.login', name='home'),
    (r'^search/', include('erp.search.urls')),
    #(r'^erp/$', include('erp.home.urls')),
    (r'^erp/home/',include('erp.home.urls')),
    #(r'^erp/users/', include('erp.users.urls')),
    #(r'^erp/dashboard/',include('erp.dashboard.urls')),	
    # Make the above 2 URLConfs look like these 2 below
	(r'^erp/(?P<owner_name>\w+)/feedback/', include('erp.feedback.urls')),
	(r'^erp/feedback/', include('erp.feedback.urls')),
	(r'^erp/finance_portal/',include('erp.finance.urls')),
<<<<<<< HEAD
=======
	(r'^erp/facilities/',include('erp.facilities.urls')),
>>>>>>> facilities_release
    (r'^erp/(?P<owner_name>\w+)/users/', include('erp.users.urls')),
    (r'^erp/(?P<owner_name>\w+)/dashboard/',include('erp.dashboard.urls')),	
    (r'^erp/(?P<owner_name>\w+)/', include('erp.tasks.urls')),
    (r'^erp/forgot_password/$', 'erp.home.views.forgot_password'),
    #(r'^loaddata/$', 'erp.dashboard.views.load_data'), #used to load test data into db.
    
    (r'^erp/media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    
    #(r'^now/sign.html$', sign_in, ),
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^task/remainder/email/$', 'erp.tasks.views.remainder', name='remainder'),
)

