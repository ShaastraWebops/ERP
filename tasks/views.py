
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from forms import TaskForm
from forms import TaskCommentForm
from models import *
# This seems necessary to avoid CSRF errors
from erp.misc.util import *
from erp.department.models import *
from erp.settings import SITE_URL

from django import forms

# TODO :
@needs_authentication
def create_task(request):
    """Handle Creation of Task using TaskForm.
    
    TODO:
    Display the creator on the Task Create / Edit page
    Is it okay if no SubTask forms are filled out?
    Cancel Create
    Save Draft
    """
    user = request.user
    dept_names = [name for name, description in DEP_CHOICES]
    subtask_exclusion_tuple = ('creator', 'status', 'description', 'task',)

    if user.groups.filter (name = 'Cores'):
        print 'Core'
    elif user.groups.filter (name = 'Coords'):
        print 'Coord'

    SubTaskFormSet = modelformset_factory (SubTask, exclude = subtask_exclusion_tuple, extra = 1)

    if request.method == 'POST':
        # Get the submitted formset
        subtaskfs = SubTaskFormSet (request.POST, prefix = 'all')
        task_form = TaskForm (request.POST)
        if task_form.is_valid ():
            # commit = False creates an object from the ModelForm,
            # instead of saving it
            new_task = task_form.save (commit = False)
            # Now, populate all model fields excluded from Task ModelForm
            new_task.creator = user
            # If the filled forms (if any) are valid
            if subtaskfs.is_valid ():
                # Save the Task object
                new_task.save ()
                # Get list of the instances
                subtasks = subtaskfs.save (commit = False)
                for subtask in subtasks:
                    # Populate all model fields excluded from SubTask ModelForm
                    # NOTE : As per ERPver_2.PDF, creator of
                    # subtask is same as creator of Task
                    subtask.creator = user
                    subtask.status = DEFAULT_STATUS
                    subtask.task = new_task
                    subtask.save ()
                # Save the many-to-many data for the formset, NOT the
                # instance. Necessary, since we used commit = False
                subtaskfs.save_m2m ()
                return HttpResponseRedirect ('%s/dashboard/home' % settings.SITE_URL)
            else:
                # One or more Forms are invalid
                pass
    else:
        # Create a blank form
        task_form = TaskForm ()
        # Create an empty Formset
        subtaskfs = SubTaskFormSet (prefix = 'all', queryset = SubTask.objects.none ())

    print 'No. of forms : ', subtaskfs.total_form_count ()
    return render_to_response('tasks/create_task.html' , locals(), context_instance = global_context (request))

def get_timeline (user):
    """
    If user is a Core, return all Tasks created by user.
    Else, return all Tasks for user's Department

    Should it be based on Department instead of Core?
    """
    # Get user's department name
    user_dept = user.userprofile_set.all()[0].department
    if user.groups.filter (name = 'Cores'):
        return Task.objects.filter (creator = user)
    else:
        return Task.objects.filter (creator__userprofile__department = user_dept)

def get_subtasks (user):
    """
    Return all SubTasks assigned to user (assumed to be a Coord).
    """
    # Return list of SubTasks for which at least one of the coords is user
    return SubTask.objects.filter (coords = user)
    
def get_unassigned_received_subtasks (user):
    """
    Return all SubTasks assigned to user's Department which have not been assigned to any Coord.
    user is assumed to be a Core.
    """
    user_dept = user.userprofile_set.all()[0].department
    return SubTask.objects.filter (department = user_dept).filter (coords = None)

def get_requested_subtasks (user):
    """
    Return all SubTasks (created by user) requested from other Departments. 

    user is assumed to be a Core.
    """
    user_dept = user.userprofile_set.all()[0].department
    # Q object used here to negate the search
    return SubTask.objects.filter (~Q (department = user_dept), creator = user)

def get_completed_subtasks (user):
    """
    Return all SubTasks completed by coords in user's Department
    """
    user_dept = user.userprofile_set.all()[0].department
    return SubTask.objects.filter (department = user_dept, status = 'C')
    

@needs_authentication
def display_portal (request):
    """
    List all Tasks created by this user

    Check whether user is authenticated.
    Assumes that the user is either a Coord or a Core.
    """
    user = request.user
    if user.groups.filter (name = 'Cores'):
        all_Tasks = get_timeline (user)
        all_unassigned_received_SubTasks = get_unassigned_received_subtasks (user)
        all_requested_SubTasks = get_requested_subtasks (user)
        all_completed_SubTasks = get_completed_subtasks (user)
        print user.username
        # print all_unassigned_received_SubTasks, all_requested_SubTasks
        return render_to_response('tasks/core_portal2.html' , locals(), context_instance = global_context (request))
    else:
        all_Tasks = get_timeline (user)
        all_SubTasks = get_subtasks (user)
        return render_to_response('tasks/coord_portal.html' , locals(), context_instance = global_context (request))

@needs_authentication
def edit_task (request, task_id):
    """
    Edit existing Task.
    TODO :
    Do user validation (should have permission)
    Allow delete SubTask facility
    Allow delete Task facility (?)
    Cancel Edit
    Save Draft
    """

    user = request.user
    dept_names = [name for name, description in DEP_CHOICES]
    subtask_exclusion_tuple = ('creator', 'status', 'description', 'task',)
    curr_task = Task.objects.get (id = task_id)

    if user.groups.filter (name = 'Cores'):
        print 'Core'
    elif user.groups.filter (name = 'Coords'):
        print 'Coord'

    SubTaskFormSet = modelformset_factory (SubTask, exclude = subtask_exclusion_tuple, extra = 1)

    if request.method == 'POST':
        # Get the submitted formset - filled with the existing
        # SubTasks of the current Task
        subtaskfs = SubTaskFormSet (request.POST, prefix = 'all', queryset = SubTask.objects.filter (task__id = int (task_id)))
        task_form = TaskForm (request.POST, instance = curr_task)
        if task_form.is_valid ():
            # If the filled forms (if any) are valid
            if subtaskfs.is_valid ():
                # Save the Task object
                task_form.save ()
                # Get list of the changed instances (including brand
                # new SubTasks instances)
                subtasks = subtaskfs.save (commit = False)
                print 'SubTasks'
                for subtask in subtasks:
                    # Populate all model fields excluded from SubTask ModelForm
                    # NOTE : As per ERPver_2.PDF, creator of
                    # subtask is same as creator of Task
                    subtask.creator = user
                    subtask.status = DEFAULT_STATUS
                    subtask.task = curr_task
                    subtask.save ()
                # Save the many-to-many data for the formset, NOT the
                # instance. Necessary, since we used commit = False
                subtaskfs.save_m2m ()
                return HttpResponseRedirect ('%s/dashboard/home' % settings.SITE_URL)
            else:
                # One or more Forms are invalid
                pass
    else:
        # Create Task form with existing values filled in
        task_form = TaskForm (instance = Task.objects.get (id = task_id))
        # Create Formset with existing values filled in
        subtaskfs = SubTaskFormSet (prefix = 'all', queryset = SubTask.objects.filter (task__id = int (task_id)))

    print 'No. of forms : ', subtaskfs.total_form_count ()
    return render_to_response('tasks/edit_task.html' , locals(), context_instance = global_context (request))

def display_subtask (request, subtask_id):
    """
    Display full details of a SubTask.
    TODO :
    Validation
    """
    curr_subtask = SubTask.objects.get (id = subtask_id)
    return render_to_response('tasks/display_subtask.html', locals(), context_instance = global_context (request))
    


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
    

    return render_to_response('tasks/assigned_task.html' , locals(), context_instance = global_context (request))
        

                
# author: Vijay Karthik
def core_portal(request):
    display_completed_tasks = False
    display_created_tasks = False
    display = False
    return render_to_response('tasks/core_portal.html', locals(), context_instance = global_context (request))

def listoftasks(request):
    """
    TODO: Fix Department
    """
    user = request.user
    objects =  Task.objects.filter(creator = user) 
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
    user = request.user
    objects = SubTask.objects.filter(creator = user, status = "Completed")      
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
    task_dict['display_completed _tasks'] = True
    return render_to_response("tasks/core_portal.html", task_dict, context_instance = global_context (request))


@needs_authentication    
def task_comment(request):
    """
    Creates a comment. Needs to be integrated with edit Task.
    A similar method can be used for subtask_comment. Will do once i get an idea
    how edit task is being implemented.
    """
    task_comment = TaskCommentForm()
    user = request.user
    if request.method == 'POST':
        task_comment = TaskCommentForm(request.POST)
        if task_comment.is_valid():
            filled_forms_valid = True        
            task_comment = TaskCommentForm (request.POST)
            new_comment = task_comment.save (commit = False)
            new_comment.creator = user
            filled_forms_valid = True
            new_comment.save ()
            return render_to_response("tasks/comments.html", {
                    "formset": task_comment, "success" : True
                    })

    return render_to_response("tasks/comments.html", {
            "formset": task_comment, "success" : False
            })
