from django.conf.urls.defaults import *
from django.views.generic.simple import *

urlpatterns = patterns('erp.feedback.views',
        (r'^answer/$', 'answer'),
        (r'^question_for/$','question_for'),
        (r'^add_question/(?P<question_for>\w+)/$', 'add_question'),
        (r'^display/(?P<question_for>\w+)/$', 'display'),
        (r'^review/$', 'review'),
        (r'^qms_review/(?P<dept_id>\d+)/$', 'qms_review'),  
        #(r'^rate/(?P<coord_name>\w+)/(?P<question_id>\d+)/$', 'rate'),
        #(r'^edit/(?P<coord_name>\w+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', 'edit'),
        (r'^delete/(?P<question_id>\d+)/$', 'delete_question'),
        (r'^display_questions/(?P<coord_id>\d+)/$','display_questions'),
        (r'^answer_questions/(?P<userprofile_id>\d+)/(?P<question_id>\d+)/(?P<rating>\d+)/$','answer_questions'),	
        )


