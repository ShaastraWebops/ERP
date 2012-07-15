from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.feedback.views',
      (r'^answer/$', 'answer'),
      (r'^add_question/$', 'add_question'),
)

