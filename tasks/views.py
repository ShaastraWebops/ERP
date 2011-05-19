# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import datetime
from forms import TaskForm
from models import *
from django.newforms import form_for_model



import forms , models

#author : vivek kumar bagaria
def assigned_task(request):
    # below one  is to be used
    #creator = request.user
    #using this until the login stuff is made
    creator="me" 
    #this will accept the new task and upload in the database
    if requets.method=='POST':
        form = new_task(request.POST)
        if form.is_valid():
            status      ="Not started"
            #initial status 
            subject     =form.cleaned_data['subject']
            description =form.cleaned_data['description']
            

            creation_date= datetime.datetime.now()
            # please check the above line , this will even give time till second accuracy
            assignee     =form.cleaned_data['assignee']
            deadline     =form.cleaned_data['deadline']
            #the above field can be obtained in a better fashion

            department   =form.cleaned_data['department']
            #please check
            #department can be taken from assignee or explicitly wrriten
            #i have taken it explicitly for time being ,we can change it
            manager      =form.cleaned_data['manager']

            data=Task(subject = subject , description = description , creator=creator, assignee =assignee ,
                      deadline=deadline , status = status , department =department ,manager=manager)
            data.save()
            # the below context is just wriiten for namesake . i know we have to use it the way
            #it is used in userportal , change it later




    context     = Context(request ,{ 'user':creator ,})
    #here the tasks which are assigned by the creator r selected and passed to the templates which will display them
    tasks_details=Task.object.filter(creator=creator)
    display_form=TaskForm()
    

    return render_to_response('tasks/assigned_task.html ' , locals() ,context_instance=context)
        
    
