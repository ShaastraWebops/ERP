from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.feedback.views',
      (r'^answer/$', 'answer'),
      (r'^add_question/$', 'add_question'),
      (r'^display/$', 'display'),
      (r'^rate/(?P<coord_name>\w+)/(?P<question_id>\d+)/$', 'rate'),
      (r'^edit/(?P<coord_name>\w+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', 'edit'),
      (r'^delete/(?P<question_id>\d+)/$', 'delete_question'),
	 	
)
	

