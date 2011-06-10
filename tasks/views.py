
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
from forms import TaskForm, SubTaskForm, TaskCommentForm, SubTaskCommentForm
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
    # Template variable
    is_new_task = True

    if user.groups.filter (name = 'Cores'):
        print 'Core'
    elif user.groups.filter (name = 'Coords'):
        print 'Coord'

    SubTaskFormSet = modelformset_factory (SubTask,
                                           exclude = subtask_exclusion_tuple,
                                           extra = 3)
    if request.method == 'POST':
        subtaskfs = SubTaskFormSet (request.POST, prefix = 'all')
        task_form = TaskForm (request.POST)
        if task_form.is_valid ():
            new_task = task_form.save (commit = False)
            new_task.creator = user
            # If the filled forms (if any) are valid
            if subtaskfs.is_valid ():
                new_task.save ()
                subtasks = subtaskfs.save (commit = False)
                for subtask in subtasks:
                    subtask.creator = user
                    subtask.status = DEFAULT_STATUS
                    subtask.task = new_task
                    subtask.save ()
                subtaskfs.save_m2m () # Necessary, since we used commit = False
                return HttpResponseRedirect ('%s/dashboard/home'
                                             % settings.SITE_URL)
            else:
                # One or more Forms are invalid
                pass
    else:
        task_form = TaskForm ()
        subtaskfs = SubTaskFormSet (prefix = 'all',
                                    queryset = SubTask.objects.none ())
    print 'No. of forms : ', subtaskfs.total_form_count ()
    return render_to_response('tasks/edit_task.html',
                              locals(),
                              context_instance = global_context (request))

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
    Return all SubTasks assigned to user's Department which have not
    been assigned to any Coord.
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
        return render_to_response('tasks/core_portal2.html',
                                  locals(),
                                  context_instance = global_context (request))
    else:
        all_Tasks = get_timeline (user)
        all_SubTasks = get_subtasks (user)
        return render_to_response('tasks/coord_portal.html',
                                  locals(),
                                  context_instance = global_context (request))

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
    # Template variable
    is_new_task = False

    if user.groups.filter (name = 'Cores'):
        print 'Core'
    elif user.groups.filter (name = 'Coords'):
        print 'Coord'





    SubTaskFormSet = modelformset_factory (SubTask,
                                           exclude = subtask_exclusion_tuple,
                                           extra = 1)
    if request.method == 'POST':
        # Get the submitted formset - filled with the existing
        # SubTasks of the current Task
        subtaskfs = SubTaskFormSet (request.POST,
                                    prefix = 'all',
                                    queryset = SubTask.objects.filter (task__id = int (task_id)))
        task_form = TaskForm (request.POST, instance = curr_task)
        if task_form.is_valid ():
            if subtaskfs.is_valid ():
                task_form.save ()
                subtasks = subtaskfs.save (commit = False)
                print 'SubTasks'
                for subtask in subtasks:
                    subtask.creator = user
                    subtask.status = DEFAULT_STATUS
                    subtask.task = curr_task
                    subtask.save ()
                subtaskfs.save_m2m ()   # Necessary, since we used commit = False
                return HttpResponseRedirect ('%s/dashboard/home' %
                                             settings.SITE_URL)
            else:
                # One or more Forms are invalid
                pass
    else:
        task_form = TaskForm (instance = Task.objects.get (id = task_id))
        subtaskfs = SubTaskFormSet (prefix = 'all',
                                    queryset = SubTask.objects.filter (task__id = int (task_id)))
    print 'No. of forms : ', subtaskfs.total_form_count ()
    return render_to_response('tasks/edit_task.html',
                              locals(),
                              context_instance = global_context (request))

@needs_authentication
def display_subtask (request, subtask_id):
    """
    Display full details of a SubTask.
    TODO :
    Validation
    """
    curr_subtask = SubTask.objects.get (id = subtask_id)
    curr_subtask_form = SubTaskForm (instance = curr_subtask)
    has_updated = False
    if request.method == 'POST':
        # Hack to get the status
        if request.POST.get ('status', 'O') != '':
            curr_subtask.status = request.POST.get ('status', 'O') 
            curr_subtask.save ()
            has_updated = True
            # Reinstantiate the form
            curr_subtask_form = SubTaskForm (instance = curr_subtask)
            print 'SubTask updated'
    return render_to_response('tasks/display_subtask.html',
                              locals(),
                              context_instance = global_context (request))
    
@needs_authentication
def display_task (request, task_id):
    """
    Display full details of a Task.
    TODO :
    Validation
    Back Button to go back
    """
    curr_task = Task.objects.get (id = task_id)
    return render_to_response('tasks/display_task.html',
                              locals(),
                              context_instance = global_context (request))
                

# Comments Part:
# Comments for Tasks and subtasks are very similar. So they call the same function.

@needs_authentication    
def handle_task_comments (request, task_id):
    """
    Displays all comments for Task of task_id and allows addition of a
    comment.

    TODO :
    Make sure that user is a Core. (Necessary?)
    """
    comment_form, status = handle_comment (request = request, is_task_comment = True, object_id = task_id)
    comments = TaskComment.objects.filter (task__id = task_id)
    curr_object = Task.objects.get (id = task_id)
    is_task_comment = True
    return render_to_response('tasks/comments.html',
                              locals(),
                              context_instance = global_context (request))

@needs_authentication    
def handle_subtask_comments (request, subtask_id):
    """
    Displays all comments for SubTask of subtask_id and allows
    addition of a comment.
    """
    comment_form, status = handle_comment (request = request, is_task_comment = False, object_id = subtask_id)
    comments = SubTaskComment.objects.filter (subtask__id = subtask_id)
    curr_object = SubTask.objects.get (id = subtask_id)
    is_task_comment = False
    return render_to_response('tasks/comments.html',
                              locals(),
                              context_instance = global_context (request))



# Adds comments to task / subtasks
def handle_comment (request, is_task_comment, object_id):
    """
    Return a tuple : (comment form, status).

    If the form was POSTed, then save the comment and return empty form, status =
    'Success'.
    If the form data is invalid, then return form and status = 'Invalid Form'
    If the object of given id was not found, status = 'Not Found'
    Else, return blank form and status = 'Blank'

    If is_task_comment is True, treat it as a TaskComment. Else, treat
    it as a SubTaskComment.
    """    
    success = False
    not_found = True
    user = request.user

    if is_task_comment:
        curr_modelform = TaskCommentForm
        curr_model = Task
    else:
        curr_modelform = SubTaskCommentForm
        curr_model = SubTask

    if request.method == 'POST':
        comment_form = curr_modelform(request.POST)            
        if comment_form.is_valid():
            new_comment = comment_form.save (commit = False)
            try:
                curr_object = curr_model.objects.get (id = object_id)
            except:
                not_found = True
                return (comment_form, 'Not Found')
            success = True
            new_comment.author = user
            if is_task_comment:
                new_comment.task = curr_object
                print 'New Comment : ', new_comment.author, new_comment.comment_string, new_comment.time_stamp, new_comment.task.subject
            else:
                new_comment.subtask = curr_object
                print 'New Comment : ', new_comment.author, new_comment.comment_string, new_comment.time_stamp, new_comment.subtask.subject
            new_comment.save ()
            # Blank the form
            comment_form = curr_modelform ()
            return (comment_form, 'Success')
        else:
            return (comment_form, 'Invalid Form')
    else:
        # Blank form
        comment_form = curr_modelform ()
    return (comment_form, 'Blank')
