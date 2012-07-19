# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from erp.misc.helper import is_core, is_coord, get_page_owner
from feedback.forms import *
from erp.users.models import *
from django.http import Http404
from erp.feedback.models import *
from django.db.models import Avg
from django.core.urlresolvers import reverse
from decimal import Decimal


def answer(request):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    if is_core(curr_user):
        is_core1=True
        is_visitor1=False
        if str(curr_userprofile.department) == "QMS":
            qms_core=True    
        curr_department=curr_userprofile.department
        coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
        questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
        answers=Answer.objects.filter(creator=curr_userprofile)
    if is_coord(curr_user):
		user_coord=True
		if str(curr_userprofile.department) == "QMS":
			qms_coord=True
		curr_department=curr_userprofile.department
		core_profiles=userprofile.objects.filter(department=curr_department,user__groups__name='Cores')
		coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords').exclude(user=request.user)
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
		answers=Answer.objects.filter(creator=curr_userprofile)           
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))

def display(request,question_for):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    if is_core(curr_user):
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
			if question_for=='Core'
				question_for_core=True
	            questions=Question.objects.filter(question_for='Core')
			else:
				questions=Question.objects.filter(question_for='Coord')	
				question_for_coord=True		
        else:
            raise Http404

    if is_coord(curr_user):
        if str(curr_userprofile.department) == "QMS":
            qms_coord=True
			if question_for=='Core'
				question_for_core=True
	            questions=Question.objects.filter(question_for='Core')
			else:
				question_for_coord=True
				questions=Question.objects.filter(question_for='Coord')			
        else:
            raise Http404
                    
    return render_to_response('feedback/display.html',locals(),context_instance=RequestContext(request))

def question_for(request):
	Core='Core'
	Coord='Coord'
	return render_to_response('feedback/questions_for.html',locals(),context_instance=RequestContext(request))

def add_question(request,question_for):
	
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        owner_name=None
        page_owner = get_page_owner (request, owner_name)
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
			if question_for== 'Coord':
            	if request.method == 'POST':
                	questionform=QuestionFormCoord(request.POST)
                	question_added=False
               		if questionform.is_valid():
						questionform1=questionform.save(commit=False)
						questionform1.creator=curr_userprofile
						questionform1.feedback_for='Coord'
						questionform1.save()
						questionform.save_m2m()
						question_added= True
                	else:
                		error=True
            	questionform=QuestionFormCoord()
            	return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
			else:
				if request.method == 'POST':
                	questionform=QuestionFormCore(request.POST)
                	question_added=False
               		if questionform.is_valid():
						questionform1=questionform.save(commit=False)
						questionform1.creator=curr_userprofile
						questionform1.feedback_for='Core'
						questionform1.answered_by='Coord'
						questionform1.save()
						questionform.save_m2m()
						question_added= True
                	else:
                		error=True
            	questionform=QuestionFormCore()
            	return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
        else:
            raise Http404
	
    if is_coord(request.user):
		owner_name=None
		page_owner = get_page_owner (request, owner_name)
		curr_userprofile=userprofile.objects.get(user=request.user)
		if str(curr_userprofile.department) == "QMS":
			qms_coord=True
			if question_for== 'Coord':
            	if request.method == 'POST':
                	questionform=QuestionFormCoord(request.POST)
                	question_added=False
               		if questionform.is_valid():
						questionform1=questionform.save(commit=False)
						questionform1.creator=curr_userprofile
						questionform1.feedback_for='Coord'
						questionform1.save()
						questionform.save_m2m()
						question_added= True
                	else:
                		error=True
            	questionform=QuestionFormCoord()
            	return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
			else:
				if request.method == 'POST':
                	questionform=QuestionFormCore(request.POST)
                	question_added=False
               		if questionform.is_valid():
						questionform1=questionform.save(commit=False)
						questionform1.creator=curr_userprofile
						questionform1.feedback_for='Core'
						questionform1.answered_by='Coord'
						questionform1.save()
						questionform.save_m2m()
						question_added= True
                	else:
                		error=True
            	questionform=QuestionFormCore()
            	return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
        else:
            raise Http404
	




def display_questions(request,coord_id):
	curr_user=request.user
	curr_userprofile=userprofile.objects.get(user=request.user)
	owner_name=None
	page_owner = get_page_owner (request, owner_name)
	curr_department=curr_userprofile.department
	curr_coord_userprofile=userprofile.objects.get(id=coord_id)
	if is_core(curr_user):
		if str(curr_userprofile.department) == "QMS":
			is_core1=True
			is_visitor1=False
			qms_core=True
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
		answers=Answer.objects.filter(creator=curr_userprofile)
		
	
	if is_coord(curr_user):
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
		answers=Answer.objects.filter(creator=curr_userprofile)

	return render_to_response('feedback/display_questions.html',locals(),context_instance=RequestContext(request))

def answer_questions(request,userprofile_id,question_id,rating=None):
	if str(rating) == '20':
		rating=None
	rating_choice=[i for i in range(11)]
	curr_user=request.user
	
	curr_userprofile=userprofile.objects.get(user=request.user)
	owner_name=None
	is_core1=False
	qms_core=False
	page_owner = get_page_owner (request, owner_name)
	curr_department=curr_userprofile.department
	answers=Answer.objects.filter(creator=curr_userprofile)
	question1=Question.objects.filter(id=question_id)
	
	if question1:
		question2=Question.objects.get(id=question_id)
	curr_feedbackuser_userprofile=userprofile.objects.get(id=userprofile_id)
	if is_core(curr_user):
		question_no_answer=[]
		if str(curr_userprofile.department) == "QMS":
			is_core1=True
			is_visitor1=False
			qms_core=True
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
		
		

			
		if rating != None:	
			answer=Answer.objects.filter(question = question2).filter(creator=curr_userprofile).filter(owner=curr_feedbackuser_userprofile)
			if answer:
				for answer1 in answer:
					answer1.rating=rating
					answer1.save()
			else:
				answer1=Answer(rating=rating,question=question2,owner=curr_feedbackuser_userprofile,creator=curr_userprofile,answered=True)
				answer1.save()
		for question_one in questions:
			answer_present=False
			for answer_one in answers:
				if answer_one.question==question_one and answer_one.creator==curr_userprofile and answer_one.owner==curr_feedbackuser_userprofile:
					answer_present=True
			if not answer_present:
				question_no_answer.append(question_one)


	
	if is_coord(curr_user):
		if str(curr_userprofile.department) == "QMS":
			qms_coord=True
		question_no_answer=[]
		if is_coord(curr_feedbackuser_userprofile.user):
			questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Coord').exclude(answered_by='Core').exclude(answered_by='Vol')
		else:
			questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Core')
		if rating != None:
			answer=Answer.objects.filter(question=question2).filter(creator=curr_userprofile).filter(owner=curr_feedbackuser_userprofile)
			if answer:
				for answer1 in answer:
					answer1.rating=rating
					answer1.save()
			else:
				answer1=Answer(rating=rating,question=question2,owner=curr_feedbackuser_userprofile,creator=curr_userprofile,answered=True)
				answer1.save()
				
		for question_one in questions:
			answer_present=False
			for answer_one in answers:
				if answer_one.question==question_one and answer_one.creator==curr_userprofile and answer_one.owner==curr_feedbackuser_userprofile:
					answer_present=True
			if not answer_present:
				question_no_answer.append(question_one)

	
	return render_to_response('feedback/answer_questions.html',locals(),context_instance=RequestContext(request))

"""
def rate(request, coord_name, question_id):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
	
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    curr_department=curr_userprofile.department
    coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
    curr_question=Question.objects.get(id=question_id)
    curr_coord_userprofile = userprofile.objects.get (name=coord_name)
#   curr_answer=Answer.objects.get(Q(question=curr_question),Q(owner=curr_coord_userprofile))
    try:
        curr_answer=Answer.objects.get(Q(question=curr_question),Q(owner=curr_coord_userprofile))
        return HttpResponseRedirect('/erp/feedback/edit/'+str(curr_coord_userprofile.name)+'/'+str(curr_question.id)+'/'+str(curr_answer.id)+'/')
    except Answer.DoesNotExist:    
        if curr_userprofile.department == curr_coord_userprofile.department:
        #Lot of repitition of code, use or statement etc. Just for checking case by case that it is foolproof
            if is_core(request.user):
                is_core1=True
                is_visitor1=False
                if str(curr_userprofile.department) == "QMS":
                    qms_core=True
                if curr_question.answered_by == 'Core':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
        
            if is_core(request.user):
                is_core1=True
                is_visitor1=False
                if str(curr_userprofile.department) == "QMS":
                    qms_core=True
                if curr_question.answered_by == 'All':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
                    
            if is_coord(request.user):
                if curr_question.answered_by == 'Coord':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
             
                        
            if is_coord(request.user):
                if curr_question.answered_by == 'All':
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))        

        else:
            raise Http404
"""

"""
def edit(request, coord_name, question_id, answer_id):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    curr_department=curr_userprofile.department
    coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
    curr_question=Question.objects.get(id=question_id)
    curr_coord_userprofile = userprofile.objects.get (name=coord_name)
    curr_answer=Answer.objects.get(id=answer_id)
    if curr_userprofile.department == curr_coord_userprofile.department:
        #Lot of repitition of code, use or statement etc. Just for checking case by case that it is foolproof
        if is_core(request.user):
            is_core1=True
            is_visitor1=False
            if str(curr_userprofile.department) == "QMS":
                qms_core=True
            if curr_question.answered_by == 'Core':       
                
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
        
        if is_core(request.user):
            is_core1=True
            is_visitor1=False
            if str(curr_userprofile.department) == "QMS":
                qms_core=True
            if curr_question.answered_by == 'All':       


                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))

                    
        if is_coord(request.user):
            if curr_question.answered_by == 'Coord':       
                 
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
           
                        
        if is_coord(request.user):
            if curr_question.answered_by == 'All':
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))     

    else:
       raise Http404
       

"""
        
def delete_question(request, question_id):
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        owner_name=None
        page_owner = get_page_owner (request, owner_name)
        if str(curr_userprofile.department) == "QMS":
            q = Question.objects.get(id=question_id)
            answers = q.answer_set.all()
            answeraverages = q.answeravg_set.all()
            for ans in answers:
                ans.delete()
            for avg in answeraverages:
                avg.delete()    
            q.delete()    
            return HttpResponseRedirect("/erp/feedback/display")
        else:
            raise Http404
    else:
        raise Http404
        
def review(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    curr_department=curr_userprofile.department
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    qms_core=False
    if str(curr_department) == "QMS" and is_core(request.user):
        all_departments=Department.objects.all()
        qms_core=True
        return render_to_response('feedback/review.html',locals(),context_instance=RequestContext(request))    
    if is_coord(request.user):
		if str(curr_userprofile.department) == "QMS":
			qms_coord=True
    questions=Question.objects.filter(departments=curr_department)
    owner_answers=Answer.objects.filter(owner=curr_userprofile)
    curr_averages = Answeravg.objects.filter(owner=curr_userprofile)
    if is_coord(request.user):
        for q in questions:
            answers = Answer.objects.filter(owner=curr_userprofile).filter(question=q)
            if answers:
                existing = Answeravg.objects.filter(owner=curr_userprofile).filter(question=q)
                if existing:
                    for i in existing:
                        curr_id = i.id
                    existing_average = Answeravg.objects.get(id=curr_id)
                    add=0
                    number=0.0
                    for a in answers:
                        number +=1.0
                        add += a.rating
                    average=Decimal(add/number)
                    existing_average.avg = average
                    existing_average.num = number
                    existing_average.save()                                    
        
                else:
                    add=0
                    number=0.0
                    for a in answers:
                        number +=1.0
                        add += a.rating
                    average=Decimal(add/number)            
                    saveavg = Answeravg(question=q,owner=curr_userprofile,avg=average, num=number)
                    saveavg.save()
        averages = Answeravg.objects.filter(owner=curr_userprofile)        
    else:
        raise Http404    
    return render_to_response('feedback/review.html',locals(),context_instance=RequestContext(request))
    
def qms_review(request, dept_id):
    owner_name=None
    curr_userprofile=userprofile.objects.get(user=request.user)
    core_department=curr_userprofile.department
    all_departments=Department.objects.all()
    page_owner = get_page_owner (request, owner_name)
    curr_department = Department.objects.get(id=dept_id)
    if str(core_department) == "QMS" and is_core(request.user):
        qms_core=True
        coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
        questions=Question.objects.filter(departments=curr_department)
        for coord in coord_profiles:
            for q in questions:
                answers = Answer.objects.filter(owner=coord).filter(question=q)
                if answers:
                    existing = Answeravg.objects.filter(owner=coord).filter(question=q)
                    if existing:
                        for i in existing:
                            curr_id = i.id
                        existing_average = Answeravg.objects.get(id=curr_id)
                        add=0
                        number=0.0
                        for a in answers:
                            number +=1.0
                            add += a.rating
                        average=Decimal(add/number)
                        existing_average.avg = average
                        existing_average.num = number
                        existing_average.save()                                    
            
                    else:
                        add=0
                        number=0.0
                        for a in answers:
                            number +=1.0
                            add += a.rating
                        average=Decimal(add/number)
                        saveavg = Answeravg(question=q,owner=coord,avg=average, num=number)
                        saveavg.save()
        averages = Answeravg.objects.all()
    else:
        raise Http404
    return render_to_response('feedback/qms_review.html',locals(),context_instance=RequestContext(request))    
