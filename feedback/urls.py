from django.views.generic.simple import *
from django.conf.urls import *

urlpatterns = patterns('erp.feedback.views',
    (r'^toggle/$', 'toggle'),
    (r'^togglereview/$', 'togglereview'),
    (r'^answer/$', 'answer'),
    (r'^questions_for/$','question_for'),
    (r'^add_question/(?P<question_for>\w+)/$', 'add_question'),
    (r'^display/(?P<question_for>\w+)/$', 'display'),
    (r'^review/$', 'review'),
    (r'^qms_review/(?P<dept_id>\d+)/(?P<is_all>\w+)/$', 'qms_review'),  
    #(r'^rate/(?P<coord_name>\w+)/(?P<question_id>\d+)/$', 'rate'),
    #(r'^edit/(?P<coord_name>\w+)/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', 'edit'),
    (r'^delete/(?P<question_id>\d+)/(?P<question_for>\w+)/$', 'delete_question'),
    (r'^edit/(?P<question_id>\d+)/(?P<question_for>\w+)/$', 'edit_question'),    
    (r'^answer_questions/(?P<userprofile_id>\d+)/(?P<question_id>\d+)/(?P<rating>\d+)/$','answer_questions'),	
)
