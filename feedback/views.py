# Create your views here.
from __future__ import division
from django.http import *
from django.shortcuts import *
from django.template import *
from erp.misc.helper import is_core, is_coord, get_page_owner
from erp.feedback.forms import *
from erp.users.models import *
from django.http import Http404
from erp.feedback.models import *
from django.db.models import Avg
from django.core.urlresolvers import reverse
from decimal import Decimal

"""
Toggle function is solely for the qms core to open/close the feedback feature
"""
def toggle(request):
    print "hello"
    curr_userprofile=userprofile.objects.get(user=request.user)
    if is_core(request.user) and str(curr_userprofile.department) == "QMS":
        openfeedback=OpenFeedback.objects.filter(id=1)
        if openfeedback:
            curr_feedback=OpenFeedback.objects.get(id=1)
        else:
            curr_feedback=OpenFeedback(feedback=False)
            curr_feedback.save()
            
        if curr_feedback.feedback==False:
            curr_feedback.feedback=True
            curr_feedback.save() 
            return redirect('erp.feedback.views.answer', )
    
        if curr_feedback.feedback==True:
            curr_feedback.feedback=False
            curr_feedback.save()
            return redirect('erp.feedback.views.answer', )        
    else:
        raise Http404  
        
"""
Togglereview function is solely for the qms core. Only if this is True can coords and cores see their reviews.
"""
def togglereview(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    if is_core(request.user) and str(curr_userprofile.department) == "QMS":
        openreview=OpenReview.objects.filter(id=1)
        if openreview:
            curr_review=OpenReview.objects.get(id=1)
        else:
            curr_review=OpenReview(review=False)
            curr_review.save()

        openfeedback=OpenFeedback.objects.filter(id=1)
        if openfeedback:
            curr_feedback=OpenFeedback.objects.get(id=1)
        else:
            curr_feedback=OpenFeedback(feedback=False)
            curr_feedback.save()
           
        if curr_review.review==False:
            curr_review.review=True
            curr_review.save()
            if curr_feedback.feedback==True:
                curr_feedback.feedback=False
                curr_feedback.save()             
            return redirect('erp.feedback.views.answer', )
    
        if curr_review.review==True:
            curr_review.review=False
            curr_review.save()
            return redirect('erp.feedback.views.answer', )        
    else:
        raise Http404                          
"""
Answer and answer_questions and review are open to all members, with different permissions.
"""
def answer(request):
    print "in answer"
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    yes='yes'
    no='no'
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    if is_core(curr_user):
        is_core1=True
        is_visitor1=False  
        if str(curr_userprofile.department) == "QMS":
            qms_core=True
            qms_dept=True
    if is_coord(curr_user):
        user_coord=True
        if str(curr_userprofile.department) == "QMS":
            qms_coord=True
            qms_dept=True             
    
    openfeedback=OpenFeedback.objects.filter(id=1)
    if openfeedback:
        curr_feedback=OpenFeedback.objects.get(id=1)
    else:
        curr_feedback=OpenFeedback(feedback=False)
        curr_feedback.save()
    
    openreview=OpenReview.objects.filter(id=1)
    if openreview:
        curr_review=OpenReview.objects.get(id=1)
    else:
        curr_review=OpenReview(review=False)
        curr_review.save()
                
    if curr_feedback.feedback==True:
   
        if is_core(curr_user):
            is_core1=True
            is_visitor1=False
            if str(curr_userprofile.department) == "QMS":
                qms_core=True 
                qms_dept=True   
            curr_department=curr_userprofile.department
            coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
            questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
            answers=Answer.objects.filter(creator=curr_userprofile)
        if is_coord(curr_user):
            user_coord=True
            if str(curr_userprofile.department) == "QMS":
                qms_coord=True
                qms_dept=True
            curr_department=curr_userprofile.department
            core_profiles=userprofile.objects.filter(department=curr_department,user__groups__name='Cores')
            coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords').exclude(user=request.user)
            questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
            answers=Answer.objects.filter(creator=curr_userprofile)           
            return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))
    
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))    
    
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
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    if is_core(curr_user):
        is_core1=True
        is_visitor1=False  
        if str(curr_userprofile.department) == "QMS":
            qms_core=True
    if is_coord(curr_user):
        user_coord=True
        if str(curr_userprofile.department) == "QMS":
            qms_coord=True      

    openfeedback=OpenFeedback.objects.filter(id=1)
    if openfeedback:
        curr_feedback=OpenFeedback.objects.get(id=1)
    else:
        curr_feedback=OpenFeedback(feedback=False)
        curr_feedback.save()
    
    if curr_feedback.feedback==True:    
        
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
            return render_to_response('feedback/answer_questions.html',locals(),context_instance=RequestContext(request))
            
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
                           
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))    

"""
A QMS Department special. To filter questions set for cores and coords.
""" 
def question_for(request):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    Core='Core'
    Coord='Coord'
    
    if str(curr_userprofile.department) == "QMS":
        if is_core(curr_user):
            qms_core=True
            is_core1=True
            is_visitor1=False
        if is_coord(curr_user):
            qms_coord=True
            is_visitor1=False

    else:
        return Http404
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

             
    return render_to_response('feedback/questions_for.html',locals(),context_instance=RequestContext(request))

"""
A QMS Department special. Displays all questions with options for editing and deleting(only for core)
"""        
def display(request,question_for):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    Core='Core'
    Coord='Coord'

    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    if is_core(curr_user):
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
            if question_for=='Core':
                question_for_core=True
                questions=Question.objects.filter(feedback_for='Core')
            else:
                questions=Question.objects.filter(feedback_for='Coord')	
                question_for_coord=True		
        else:
            raise Http404

    if is_coord(curr_user):
        if str(curr_userprofile.department) == "QMS":
            qms_coord=True
            if question_for=='Core':
                question_for_core=True
                questions=Question.objects.filter(feedback_for='Core')
            else:
                question_for_coord=True
                questions=Question.objects.filter(feedback_for='Coord')			
        else:
            raise Http404

    return render_to_response('feedback/display.html',locals(),context_instance=RequestContext(request))

"""
A QMS Department special. To add questions.
""" 
def add_question(request,question_for):

    #Get Department Members' image thumbnails
    page_owner = get_page_owner (request, owner_name=None)
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
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
                        questionform1.edited_last=curr_userprofile
                        questionform1.feedback_for='Coord'
                        questionform1.save()
                        questionform.save_m2m()
                        question_added= True
                    else:
                        error=True
                questionform=QuestionFormCoord()
                return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
            if question_for== 'Core':
                if request.method == 'POST':
                    questionform=QuestionFormCore(request.POST)
                    question_added=False
                    if questionform.is_valid():
                        questionform1=questionform.save(commit=False)
                        questionform1.creator=curr_userprofile
                        questionform1.edited_last=curr_userprofile
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
                        questionform1.edited_last=curr_userprofile
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
                        questionform1.edited_last=curr_userprofile
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

"""
A QMS department special. Similar to add_questions, but updates last edited by column also.
""" 
def edit_question(request,question_id, question_for):
    q = Question.objects.get(id=question_id)
    
    #Get Department Members' image thumbnails
    page_owner = get_page_owner (request, owner_name=None)
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
            if question_for== 'Coord':
                if request.method == 'POST':
                    questionform=QuestionFormCoord(request.POST, instance=q)
                    question_added=False
                    if questionform.is_valid():
                        questionform1=questionform.save(commit=False)
                        questionform1.edited_last=curr_userprofile
                        questionform1.feedback_for='Coord'
                        questionform1.save()
                        questionform.save_m2m()
                        question_added= True
                        return redirect('erp.feedback.views.display', question_for=question_for, permanent=True)
                    else:
                        error=True
                questionform=QuestionFormCoord(instance=q)
                return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
            if question_for== 'Core':
                if request.method == 'POST':
                    questionform=QuestionFormCore(request.POST, instance=q)
                    question_added=False
                    if questionform.is_valid():
                        questionform1=questionform.save(commit=False)
                        questionform1.edited_last=curr_userprofile
                        questionform1.feedback_for='Core'
                        questionform1.answered_by='Coord'
                        questionform1.save()
                        questionform.save_m2m()
                        question_added= True
                        return redirect('erp.feedback.views.display', question_for=question_for, permanent=True)
                    else:
                        error=True
                questionform=QuestionFormCore(instance=q)
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
                    questionform=QuestionFormCoord(request.POST,instance=q)
                    question_added=False
                    if questionform.is_valid():
                        questionform1=questionform.save(commit=False)
                        questionform1.edited_last=curr_userprofile
                        questionform1.feedback_for='Coord'
                        questionform1.save()
                        questionform.save_m2m()
                        question_added= True
                        return redirect('erp.feedback.views.display', question_for=question_for, permanent=True)
                    else:
                        error=True
                questionform=QuestionFormCoord(instance=q)
                return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
            else:
                if request.method == 'POST':
                    questionform=QuestionFormCore(request.POST, instance=q)
                    question_added=False
                    if questionform.is_valid():
                        questionform1=questionform.save(commit=False)
                        questionform1.edited_last=curr_userprofile
                        questionform1.feedback_for='Core'
                        questionform1.answered_by='Coord'
                        questionform1.save()
                        questionform.save_m2m()
                        question_added= True
                        return redirect('erp.feedback.views.display', question_for=question_for, permanent=True)
                    else:
                        error=True
                questionform=QuestionFormCore(instance=q)
                return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
        else:
            raise Http404

"""
A QMS core special.
""" 
def delete_question(request, question_id, question_for):
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        owner_name=None
        page_owner = get_page_owner (request, owner_name)
        if str(curr_userprofile.department) == "QMS":
            q = Question.objects.get(id=question_id)
            answers = q.answer_set.all()
            answeraverages = q.answeravg_set.all()
            if answers:
                for ans in answers:
                    ans.delete()
            if answeraverages:                    
                for avg in answeraverages:
                    avg.delete()    
            q.delete()
            
            return redirect('erp.feedback.views.display', question_for=question_for, permanent=True)
        else:
            raise Http404
    else:
        raise Http404

"""
The following views are for feedback reviews.
"""            
def review(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    curr_department=curr_userprofile.department
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    qms_core=False
    owner_answers=Answer.objects.filter(owner=curr_userprofile)
    curr_averages = Answeravg.objects.filter(owner=curr_userprofile)

    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    if is_core(request.user):
        is_core1=True
        is_visitor1=False
        if str(curr_department) == "QMS":
            qms_core=True
        questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Core')
    if is_coord(request.user):
        is_coord1=True
        if str(curr_userprofile.department) == "QMS":
            qms_coord=True
        questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Coord')
    
    openfeedback=OpenFeedback.objects.filter(id=1)
    if openfeedback:
        curr_feedback=OpenFeedback.objects.get(id=1)
    else:
        curr_feedback=OpenFeedback(feedback=False)
        curr_feedback.save()
                    
    openreview=OpenReview.objects.filter(id=1)
    if openreview:
        curr_review=OpenReview.objects.get(id=1)
    else:
        curr_review=OpenReview(review=False)
        curr_review.save()
    illegal=True
    if curr_review.review==True:        
        if is_core(request.user) or is_coord(request.user):
            for q in questions:            
                answers = Answer.objects.filter(owner=curr_userprofile).filter(question=q)
                if answers:
                    existing = Answeravg.objects.filter(owner=curr_userprofile).filter(question=q)
                    if existing:
                        for i in existing:
                            curr_id = i.id
                        existing_average = Answeravg.objects.get(id=curr_id)
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)
                        existing_average.avg = average
                        existing_average.num = number
                        existing_average.save()                                    
                    else:
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)            
                        saveavg = Answeravg(question=q,owner=curr_userprofile,avg=average, num=number)
                        saveavg.save()        
            averages = Answeravg.objects.filter(owner=curr_userprofile)
            return render_to_response('feedback/review.html',locals(),context_instance=RequestContext(request))        
        else:
            raise Http404    
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))      


def qms_review(request, dept_id, is_all):
    owner_name=None
    curr_userprofile=userprofile.objects.get(user=request.user)
    qms_department=curr_userprofile.department
    all_departments=Department.objects.all()
    page_owner = get_page_owner (request, owner_name)
    curr_department = Department.objects.get(id=dept_id)
    yes='yes'
    no='no'
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    if is_core(request.user):
        is_core1=True
        is_visitor1=False    
        if str(qms_department) == "QMS":
            qms_core=True
            qms_dept=True
    if is_coord(request.user) and str(qms_department) == "QMS":
        qms_dept=True
        qms_coord=True
    if is_coord(request.user) or is_core(request.user) and str(qms_department) == "QMS":            
        core_profiles=userprofile.objects.filter(department=curr_department,user__groups__name='Cores')
        coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
        for coord in coord_profiles:
            questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Coord')
            for q in questions:
                answers = Answer.objects.filter(owner=coord).filter(question=q)
                if answers:
                    existing = Answeravg.objects.filter(owner=coord).filter(question=q)
                    if existing:
                        for i in existing:
                            curr_id = i.id
                        existing_average = Answeravg.objects.get(id=curr_id)
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)
                        existing_average.avg = average
                        existing_average.num = number
                        existing_average.save()                                    

                    else:
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)
                        saveavg = Answeravg(question=q,owner=coord,avg=average, num=number)
                        saveavg.save()
        
        for core in core_profiles:
            questions=Question.objects.filter(departments=curr_department).filter(feedback_for='Core')
            for q in questions:
                answers = Answer.objects.filter(owner=core).filter(question=q)
                if answers:
                    existing = Answeravg.objects.filter(owner=core).filter(question=q)
                    if existing:
                        for i in existing:
                            curr_id = i.id
                        existing_average = Answeravg.objects.get(id=curr_id)
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)
                        existing_average.avg = average
                        existing_average.num = number
                        existing_average.save()                                    

                    else:
                        add=0
                        number=0
                        for a in answers:
                            number +=1
                            add += a.rating
                        average=Decimal(add/number)
                        saveavg = Answeravg(question=q,owner=core,avg=average, num=number)
                        saveavg.save()        
        questions=Question.objects.filter(departments=curr_department)       
        averages = Answeravg.objects.all()
    else:
        raise Http404
    return render_to_response('feedback/qms_review.html',locals(),context_instance=RequestContext(request))    
