# Create your views here.
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
# from django.http import HttpResponse, HttpResponseRedirect
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
from erp.misc.util import *
from erp.misc.helper import is_core, is_coord, get_page_owner, check_dir
from erp.department.models import *
from erp.settings import SITE_URL
from erp.dashboard.forms import shout_box_form
from erp.dashboard.models import shout_box

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
    if is_core (user):
        return Task.objects.filter (creator = user)
    else:
        return Task.objects.filter (creator__userprofile__department = user_dept)

def get_subtasks (user):
    """
    Return all SubTasks assigned to user (assumed to be a Coord).
    """
    # Return list of SubTasks for which one of the coords is user
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
    Display owner's portal.
    """
    page_owner = get_page_owner (request, owner_name)
    check_dir(request)

    if is_core (page_owner):
        return display_core_portal (request, page_owner)
    else:
        return display_coord_portal (request, page_owner)

@permissions
def display_core_portal (request, core):
    """
    Display core's portal
    """
# The case that a coord is trying to see a core's dashboard, which should'nt be allowed.      
    print "it wont come here"
    display_dict = dict ()
    # Deal with the Updates part (viewing, creating) of the portal
    update_dict = handle_updates (request, core)
    department = core.get_profile ().department
    display_dict['all_Tasks'] = get_timeline (core)
    display_dict['all_unassigned_received_SubTasks'] = get_unassigned_received_subtasks (core)
    display_dict['all_requested_SubTasks'] = get_requested_subtasks (core)
    display_dict['all_completed_SubTasks'] = get_completed_subtasks (core)
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    # Include the key-value pairs in update_dict
    display_dict.update (update_dict)
    return render_to_response('tasks/core_portal2.html',
                                  display_dict,
                                  context_instance = global_context (request))
    
def display_coord_portal (request, coord):
    """
    Display coord's portal
    """
    display_dict = dict ()
    # Deal with the Updates part (viewing, creating) of the portal
    update_dict = handle_updates (request, coord)
    department = coord.get_profile ().department
    display_dict['all_Tasks'] = get_timeline (coord)
    display_dict['all_SubTasks'] = get_subtasks (coord)
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    # Include the key-value pairs in update_dict
    display_dict.update (update_dict)
    return render_to_response('tasks/coord_portal.html',
                              display_dict,
                              context_instance = global_context (request))

# The page owner only decorator ensures that only owners of a
# Task can edit the Task (and that too only in their own page, ie. not
# while visiting some other user's page)
@needs_authentication
@page_owner_only (alternate_view_name = '')
def edit_task (request, task_id = None, owner_name = None):
    """
    Edit existing Task.

    TODO :
    Do user validation (should have permission)
    Allow delete Task facility (?)
    Cancel Edit
    Save Draft
    """

    page_owner = get_page_owner (request, owner_name)
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

    # curr_object = Task.objects.get (id = task_id)
    is_task_comment = True
    other_errors = False

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
        if task_form.is_valid () and subtaskfs.is_valid ():
            curr_task = task_form.save (commit = False)
            curr_task.save()
            print 'Task : ', curr_task

            comments, comment_form, comment_status = handle_comment (
                request = request,
                is_task_comment = True,
                object_id = task_id)

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
            return redirect ('erp.tasks.views.display_portal',
                             owner_name = owner_name)
        else:
            # One or more Forms are invalid
            other_errors = True
    else:
        task_form = TaskForm (instance = curr_task)
        subtaskfs = SubTaskFormSet (instance = curr_task)
        template_form = subtaskfs.empty_form
    comments, comment_form, comment_status = handle_comment (
        request = request,
        is_task_comment = True,
        object_id = task_id,
        other_errors = other_errors)
    return render_to_response('tasks/edit_task.html',
                              locals(),
                              context_instance = global_context (request))

@needs_authentication
@page_owner_only (alternate_view_name = '')
def edit_subtask (request, subtask_id, owner_name = None):
    """
    Display full details of a SubTask.

    Note :
    Only owners of a subtask can (fully) edit the subtask (and that too only
    in their own page, ie. not while visiting some other user's page)

    Coords who have been assigned the SubTask can change only the Status.

    TODO :
    Validation
    Have an Edit Subtask view (like for Tasks)?
    """
    page_owner = get_page_owner (request, owner_name)

    user = request.user
    curr_subtask = SubTask.objects.get (id = subtask_id)
    curr_subtask_form = SubTaskForm (instance = curr_subtask)

    if curr_subtask.is_owner (user):
        is_owner = True
    else:
        # User is a Coord
        is_owner = False

    has_updated = False
    other_errors = False
    if request.method == 'POST':
        if is_owner:
            # Let the Core save the SubTask
            curr_subtask_form = SubTaskForm (request.POST, instance = curr_subtask)
            if curr_subtask_form.is_valid ():
                curr_subtask_form.save ()
                has_updated = True
            else:
                other_errors = True
        elif 'status' in request.POST:
            # Coord - allowed to change only the status
            curr_subtask.status = request.POST.get ('status', 'O') 
            curr_subtask.save ()
            has_updated = True
            # Reinstantiate the form
            curr_subtask_form = SubTaskForm (instance = curr_subtask)
            print 'SubTask updated'
    comments, comment_form, comment_status = handle_comment (
        request = request,
        is_task_comment = False,
        object_id = subtask_id,
        other_errors = other_errors)
    if has_updated:
        return redirect ('erp.tasks.views.display_portal',
                         owner_name = owner_name)
    else:
        return render_to_response('tasks/edit_subtask.html',
                              locals(),
                              context_instance = global_context (request))

@needs_authentication
def display_subtask (request, subtask_id, owner_name = None):
    """
    Display full details of a SubTask.
    TODO :
    Validation
    Have an Edit Subtask view (like for Tasks)?
    """
    page_owner = get_page_owner (request, owner_name)
    user = request.user
    curr_subtask = SubTask.objects.get (id = subtask_id)
    comments = SubTaskComment.objects.filter (subtask__id = subtask_id)

    return render_to_response('tasks/display_subtask.html',
                              locals(),
                              context_instance = global_context (request))
    
@needs_authentication
def display_task (request, task_id, owner_name = None):
    """
    Display full details of a Task.
    TODO :
    Validation
    Back Button to go back
    """
    page_owner = get_page_owner (request, owner_name)
    print 'Display Task - Task ID : ', task_id
    curr_task = Task.objects.get (id = task_id)
    comments = TaskComment.objects.filter (task__id = task_id)
    return render_to_response('tasks/display_task.html',
                              locals(),
                              context_instance = global_context (request))

# Adds comments to task / subtasks
def handle_comment (request, is_task_comment, object_id, other_errors = False):
    """
    Return a tuple : (comments, comment form, status).

    comments : Comments for that object, if it exists. Else, None.
    other_errors : Whether the rest of the Task / SubTask form has
    errors. In that case, just keep the comment form content as is.

    If the form was POSTed, then save the comment and return comments,
    empty form, status = 'Success'.

    If the form data is invalid (ie. if it is blank) or if
    other_errors is True, then return status as 'Error'

    Else, return blank form and status = 'Blank'

    If is_task_comment is True, treat it as a TaskComment.
    Else, treat it as a SubTaskComment.
    """    
    success = False
    not_found = True
    user = request.user


    if is_task_comment:
        curr_modelform = TaskCommentForm
        curr_model = Task
        comments = TaskComment.objects.filter (task__id = object_id)
    else:
        curr_modelform = SubTaskCommentForm
        curr_model = SubTask
        comments = SubTaskComment.objects.filter (subtask__id = object_id)

    if request.method == 'POST':
        comment_form = curr_modelform (request.POST)            
        if not other_errors and comment_form.is_valid():
            new_comment = comment_form.save (commit = False)
            curr_object = curr_model.objects.get (id = object_id)
            success = True
            new_comment.author = user
            if is_task_comment:
                new_comment.task = curr_object
            else:
                new_comment.subtask = curr_object
            new_comment.save ()
            # Blank the form
            comment_form = curr_modelform ()
            return (comments, comment_form, 'Success')
        else:
            return (comments, comment_form, 'Error')
    else:
        # Blank form
        comment_form = curr_modelform ()
    return (comments, comment_form, 'Blank')

def handle_updates (request, owner_name = None):
    """
    Used by coords to send updates to Core.
    Cores will just see the updates they have received.

    Return a dict containing update variables.
    """
    page_owner = get_page_owner (request, owner_name)

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
def display_department_portal (request, owner_name = None, department_name = None):
    """
    Display all basic info about user's Department.
    """
    print 'Department name :', department_name
    # #added by vivek
    print "departmental portal here"
    shout_form=shout_box_form()
    shouts=shout_box.objects.all()
    print "done"

    page_owner = get_page_owner (request, owner_name)

    if request.method == 'POST':
        shout_form=shout_box_form (request.POST)            
        if shout_form.is_valid():
            new_shout = shout_form.save (commit = False)
            new_shout.user=page_owner
            new_shout.nickname=page_owner.get_profile ().nickname
            new_shout.timestamp=datetime.datetime.now()
            new_shout.save ()
            shout_form = shout_box_form ()
        
    if department_name is None:
        department = page_owner.get_profile ().department
    else:
        department = Department.objects.get (department_name)
    display_dict = dict ()
    display_dict['shouts']=shouts#by vivek
    display_dict['shout_form']=shout_form#by vivek
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
