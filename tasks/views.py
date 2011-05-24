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

from django import forms

def create_task(request):
    """Handle Creation of Task using TaskForm.
    
    """
    form = TaskForm ()
    user = request.user
    print user.is_authenticated()
    return render_to_response('tasks/create_task.html' , locals())

def timeline (request):
    """ List all Tasks created by this user

    (assumed to be Core as of now)
    """
    user = request.user
    all_Tasks = Task.objects.filter ()
    # all_Tasks = Task.objects.filter (creator = user)
    return render_to_response('tasks/core_portal2.html' , locals())

#author : vivek kumar bagaria
def assign_task(request):
    # below one  is to be used
    #creator = request.user
    #using this until the login stuff is made
    #creator="me" 
    #this will accept the new task and upload in the database
    if request.method=='POST':
        form = TaskForm(request.POST)
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




    context     = Context(request ,{ 'user':"me" ,})
    #here the tasks which are assigned by the creator r selected and passed to the templates which will display them
    tasks_details=models.Task.objects.all()
    display_form=TaskForm()
    

    return render_to_response('tasks/assigned_task.html' , locals() ,context_instance=context)
        

                
# author: Vijay Karthik
def core_portal(request):
    display_completed_tasks = False
    display_created_tasks = False
    display = False
    return render_to_response('tasks/core_portal.html', locals())

def listoftasks(request):
    objects =  Task.objects.filter(creator = 1)      # NEEDS to be changed  
    tasks = {}
    d = []
    for row in objects:
        ds = []
        sub_task = SubTask.objects.filter(task = row)
        for subrow in sub_task:
            cs = []
            cs.append(subrow.subject)
            cs.append(subrow.description)
            cs.append(subrow.creator)
            cs.append(subrow.creation_date)
            cs.append(subrow.deadline)
            cs.append(subrow.status)            
            cs.append(subrow.coords) # NEEDS proper representation.
            try:
                cs.append(Department.objects.get(Dept_Name = subrow.department.Dept_Name).Dept_Name)
            except:
                cs.append("unknown")
            ds.append(cs)
        c = []
        c.append(row.subject)
        c.append(row.description)
        c.append(row.creator)
        c.append(row.creation_date)
        c.append(row.deadline)
        c.append(row.status)
        c.append(ds)
        d.append(c)
    task_dict = {'tasks' : d}
    task_dict['display_created_tasks'] = True
    task_dict['display_completed_tasks'] = False
    return render_to_response("tasks/core_portal.html", task_dict)

def completedsubtasks(request):
    ds = []
    objects = SubTask.objects.filter(creator = 1, status = "Completed")      # Creator NEEDS to be changed  
    for subrow in objects:
        cs = []
        cs.append(subrow.subject)
        cs.append(subrow.description)
        cs.append(subrow.creator)
        cs.append(subrow.creation_date)
        cs.append(subrow.deadline)
        cs.append(subrow.status)            
        cs.append(subrow.coords) # NEEDS proper representation.
        try:
            cs.append(Department.objects.get(Dept_Name = subrow.department.Dept_Name).Dept_Name)
        except:
            cs.append("unknown")
        ds.append(cs)
    task_dict = {'subtasks' : ds}
    task_dict['display_created_tasks'] = False
    task_dict['display_completed_tasks'] = True
    return render_to_response("tasks/core_portal.html", task_dict)
