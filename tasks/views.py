# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.forms.models import modelformset_factory, inlineformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from forms import TaskForm, SubTaskForm, TaskCommentForm, SubTaskCommentForm, UpdateForm
from models import *
# This seems necessary to avoid CSRF errors
from erp.misc.util import *
from erp.department.models import *
from erp.settings import SITE_URL
# from erp.dashboard.forms import shout_box_form
# from erp.dashboard.models import shout_box

from django import forms

# Fields to be excluded in the SubTask forms during Task editing
subtask_exclusion_tuple = ('creator', 'status', 'description', 'task',)

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
    Return all SubTasks (created by user) sent as a request to other Departments. 

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
def display_portal (request, owner_name = None):
    """
    List all Tasks created by this user

    Check whether user is authenticated.
    Assumes that the user is either a Coord or a Core.
    """
    if owner_name is None:
        page_owner = request.user
        is_visitor = False
    else:
        page_owner = User.objects.get (username = owner_name)
        is_visitor = True

    request.session['page_owner'] = page_owner
    request.session['is_visitor'] = is_visitor

    print 'User : ', request.user.username
    print 'Page Owner : ', page_owner.username

    # Deal with the Updates part (viewing, creating) of the portal
    update_dict = handle_updates (request, page_owner)

    display_dict = dict ()
    if page_owner.groups.filter (name = 'Cores'):
        # For Cores
        display_dict['all_Tasks'] = get_timeline (page_owner)
        display_dict['all_unassigned_received_SubTasks'] = get_unassigned_received_subtasks (page_owner)
        display_dict['all_requested_SubTasks'] = get_requested_subtasks (page_owner)
        display_dict['all_completed_SubTasks'] = get_completed_subtasks (page_owner)
        # Include the key-value pairs in update_dict
        display_dict.update (update_dict)
        return render_to_response('tasks/core_portal2.html',
                                  # locals(),
                                  display_dict,
                                  context_instance = global_context (request))
    else:
        # For Coords
        display_dict['all_Tasks'] = get_timeline (page_owner)
        display_dict['all_SubTasks'] = get_subtasks (page_owner)
        # Include the key-value pairs in update_dict
        display_dict.update (update_dict)
        return render_to_response('tasks/coord_portal.html',
                                  # locals(),
                                  display_dict,
                                  context_instance = global_context (request))
@needs_authentication
def edit_task (request, task_id = False):
    """
    Edit existing Task.
    TODO :
    Do user validation (should have permission)
    Allow delete Task facility (?)
    Cancel Edit
    Save Draft
    """

    if request.session.get ('is_visitor', False):
        return display_task (request, task_id)
    user = request.user
    dept_names = [name for name, description in DEP_CHOICES]
    if task_id:
        # Existing Task
        curr_task = Task.objects.get (id = task_id)
        is_new_task = False
    else:
        # New Task
        curr_task = Task (creator = user)
        is_new_task = True

    SubTaskFormSet = inlineformset_factory (Task,
                                            SubTask,
                                            form = SubTaskForm,
                                            exclude = subtask_exclusion_tuple,
                                            extra = 0,
                                            can_delete = True)
    if request.method == 'POST':
        # Get the submitted formset
        subtaskfs = SubTaskFormSet (request.POST,
                                    instance = curr_task)
        template_form = subtaskfs.empty_form
        task_form = TaskForm (request.POST, instance = curr_task)
        if task_form.is_valid ():
            if subtaskfs.is_valid ():
                curr_task = task_form.save (commit = False)
                curr_task.save()
                print 'Task : ', curr_task

                # Only the filled forms will be stored in subtasks
                # Also, subtasks marked for deletion are deleted here.
                subtasks = subtaskfs.save (commit = False)
                for subtask in subtasks:
                    print 'Subtask : ', subtask
                    subtask.creator = user
                    subtask.status = DEFAULT_STATUS
                    # In case it's a new form (inline formset won't
                    # fill in the task in that case)
                    subtask.task = curr_task
                    subtask.save ()
                subtaskfs.save_m2m () # Necessary, since we used commit = False
                return HttpResponseRedirect ('%s/dashboard/home'
                                             % settings.SITE_URL)
            else:
                # One or more Forms are invalid
                pass
    else:
        task_form = TaskForm (instance = curr_task)
        subtaskfs = SubTaskFormSet (instance = curr_task)
        template_form = subtaskfs.empty_form
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
    user = request.user
    curr_subtask = SubTask.objects.get (id = subtask_id)
    curr_subtask_form = SubTaskForm (instance = curr_subtask)

    if user.groups.filter (name = 'Cores'):
        if curr_subtask.task.creator == user:
            is_creator = True
        elif curr_subtask.department == user.get_profile ().department:
            is_assignee = True

    has_updated = False
    if request.method == 'POST':
        if is_creator or is_assignee:
            # Let the Core save the SubTask
            curr_subtask_form = SubTaskForm (request.POST, instance = curr_subtask)
            if curr_subtask_form.is_valid ():
                curr_subtask_form.save ()
                return HttpResponseRedirect ('%s/dashboard/home' %
                                             settings.SITE_URL)
        else:
            # CHANGE - status is now a dropdown box
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
    comment_form, comment_status = handle_comment (request = request, is_task_comment = True, object_id = task_id)
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
    comment_form, comment_status = handle_comment (request = request, is_task_comment = False, object_id = subtask_id)
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
            else:
                new_comment.subtask = curr_object
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

@needs_authentication
def handle_updates (request, page_owner = None):
    """
    Used by coords to send updates to Core.
    Cores will just see the updates they have received.

    Return a dict containing update variables.
    """
    if page_owner is None:
        page_owner = request.user

    update_dict = dict ()
    if page_owner.groups.filter (name = 'Coords'):
        # For Coords
        update_form = UpdateForm ()
        update_status = "Blank"
        update_dict['updates'] = Update.objects.filter (author = page_owner)
        update_dict['update_form'] = update_form
        update_dict['update_status'] = update_status
    else:
        # For Core, just display all updates for his dept
        update_dict['updates'] = get_all_updates (
            page_owner.get_profile ().department)

    if request.method == 'POST':
        update_form = UpdateForm (request.POST)            
        if update_form.is_valid():
            new_update = update_form.save (commit = False)
            new_update.author = page_owner
            new_update.save ()
            update_form = UpdateForm ()
            update_status = "Success"
            update_dict['update_status'] = update_status
            return update_dict
        else:
            update_status = "Failed"
            update_dict['update_status'] = update_status
            update_dict['update_form'] = update_form
            return update_dict
    return update_dict

def get_all_updates (dept):
    """
    Return all updates for department dept.
    """
    return Update.objects.filter (author__userprofile__department = dept)

@needs_authentication
def display_department_portal (request, owner_name = None):
    """
    Display all basic info about user's Department.
    """
    # #added by vivek
    # print "departmental portal here"
    # shout_form=shout_box_form()
    # shouts=shout_box.objects.all()
    # print "done"

    if owner_name is None:
        page_owner = request.user
        is_visitor = False
    else:
        print 'Owner name : ', owner_name
        page_owner = User.objects.get (username = owner_name)
        is_visitor = True

    request.session['page_owner'] = page_owner
    request.session['is_visitor'] = is_visitor

    department = page_owner.get_profile ().department
    display_dict = dict ()
    # display_dict['shouts']=shouts#by vivek
    # display_dict['shout_form']=shout_form#by vivek
    display_dict['all_Tasks'] = get_timeline (page_owner)
    display_dict['updates'] = get_all_updates (department)
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    return render_to_response('tasks/department_portal.html',
                              display_dict,
                              context_instance = global_context (request))
