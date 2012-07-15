# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from erp.misc.helper import is_core, is_coord, get_page_owner
from feedback.forms import *
from erp.users.models import *
from django.http import Http404
from erp.feedback.models import *


def answer(request):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    if is_core(curr_user):
		curr_department=curr_userprofile.department
		coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))

def add_question(request):
	if is_core(request.user):
		curr_userprofile=userprofile.objects.get(user=request.user)
		owner_name=None
		page_owner = get_page_owner (request, owner_name)
		if str(curr_userprofile.department) == "QMS":
			if request.method == 'POST':
				questionform=QuestionForm(request.POST)
				question_added=False
				if questionform.is_valid():
					questionform.save()
					question_added= True
				else:
					error=True
				
	
			questionform=QuestionForm()
			return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
		else:
			raise Http404
	else:
		raise Http404    
