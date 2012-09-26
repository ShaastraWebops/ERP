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
from django.contrib.auth.models import User
from datetime import date
from forms import TaskForm, SubTaskForm, TaskCommentForm, SubTaskCommentForm, UpdateForm
from models import *
from erp.misc.util import *
from erp.misc.helper import is_core, is_coord, get_page_owner
from erp.department.models import *
from erp.settings import SITE_URL
from erp.dashboard.forms import shout_box_form
from erp.dashboard.models import shout_box
from django import forms
from django.core.mail import *
from erp.users.models import *
from django.template.loader import get_template
from django.template import Context
from django.core import mail
from django.http import HttpResponse
from dateutil.relativedelta import *
from ajax import *
from django.utils.functional import curry
from department.models import *
from misc.helper import is_core
from django.contrib.sessions.models import Session
# Fields to be excluded in the SubTask forms during Task editing
subtask_exclusion_tuple = ('creator', 'status', 'description', 'task',)

@needs_authentication_multiple_user
def multiple_login(request, owner_name=None, department=None):
    if is_core(request.user):
        group_name='Core'
    else:
        group_name='Coord'
    dept=Department.objects.filter(Dept_Name=department)[0]
    if (request.user.get_profile().department):
            multiple_user = False
    else:
        auth.logout(request)
        try:
            response.set_cookie('logged_out', 1)
        except:
            pass
        print "THe department is", department
        dept = Department.objects.get(Dept_Name=department)
        multiple = userprofile.objects.filter(department=dept)
        for each in multiple:              
            if each.user.username.startswith(owner_name.lower()) and each.user.username.endswith(department.lower()):    
                # Hard code this or write a backend?
                auth.logout(request)
                each.user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login (request, each.user)
                request.session['logged_in'] = True
                try:
                    response.set_cookie('logged_out', 0)
                except:
                    pass
                #HttpResponseRedirect('/')    
                return redirect ('erp.tasks.views.display_portal',
                                 owner_name = each.user.username)
    return HttpResponseRedirect('/')                

@needs_authentication_multiple_user    
def multiple_logout(request, owner_name=None):
    superuser = request.user
    if owner_name==request.user.username:
        if is_core (request.user):
            supercorelist = request.user.get_profile().department.owner.all()

            for each in supercorelist:
                print owner_name, each
                if owner_name.startswith(each.username.lower()):
                    superuser=each
                    print superuser
                    auth.logout(request)
                    superuser.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, superuser)
                    request.session['logged_in'] = True
                    try:
                        response.set_cookie('logged_out', 0)
                    except:
                        pass
                    break

        else:
            dept = request.user.get_profile().department
            if request.user.username.endswith(dept.Dept_Name.lower()):
                multiple_coord = request.user.username.split('_')[0]
                superuser = User.objects.get(username = multiple_coord)
                auth.logout(request)
                superuser.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, superuser)
                request.session['logged_in'] = True
                try:
                    response.set_cookie('logged_out', 0)
                except:
                    pass
    else:
        superuser=request.user
    return redirect ('erp.tasks.views.display_portal',
                                 owner_name = superuser.username)

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

@needs_authentication_multiple_user
def display_portal (request, owner_name = None):
    """
    Display owner's portal.
    """
    page_owner = get_page_owner (request, owner_name)

    if is_multiple_user (page_owner):
        return display_multiple_portal (request, page_owner)
    elif is_core (page_owner):
        return display_core_portal (request, page_owner)
    elif is_supercoord(page_owner):
        return display_supercoord_portal (request, page_owner)
    elif is_coord(page_owner):
        return display_coord_portal (request, page_owner)       

@permissions
def display_multiple_portal (request, user):
    """
    Display the portal so Core/coord can login into respective events
    """
    if is_core (request.user):
        depts = list(user.department_set.all())
    else:
        depts=[]
        multiple = userprofile.objects.all()
        for each in multiple:              
            if each.user.username.startswith(user.username.lower()+'_'):
                depts.append(each.department)
    return render_to_response("tasks/multiple.html",locals(), context_instance=global_context(request))

@permissions
def display_core_portal (request, core):
    """
    Display core's portal
    """
    display_dict = dict ()

    if request.method == "POST":
        if 'delete' in request.POST:
            delete_tasks=request.POST.getlist('delete_tasks')
            for i in delete_tasks:
                deltask=Task.objects.get(pk=i)
                for delcomment in deltask.taskcomment_set.all():
                    delcomment.delete()
                for delsubtask in deltask.subtask_set.all():
                    for delsubtaskcomment in delsubtask.subtaskcomment_set.all():
                        delsubtaskcomment.delete()
                    delsubtask.delete()
                deltask.delete()
            display_dict['tasks_deleted'] = True
                
    # Deal with the Updates part (viewing, creating) of the portal
    update_dict = handle_updates (request, core)
    department = core.get_profile ().department
    display_dict['all_Tasks'] = get_timeline (core)
    display_dict['all_unassigned_received_SubTasks'] = get_unassigned_received_subtasks (core)
    display_dict['all_requested_SubTasks'] = get_requested_subtasks (core)
    display_dict['all_completed_SubTasks'] = get_completed_subtasks (core)
    
    
    #Get Department Members' image thumbnails
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_supercoords_list'] = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
        
    qms_core=False
    curr_userprofile=userprofile.objects.get(user=request.user)
    if str(department) == 'QMS':
		display_dict['qms_core']=True
    
    # Include the key-value pairs in update_dict
    display_dict.update (update_dict)
    return render_to_response('tasks/core_portal2.html',
                                  display_dict,
                                  context_instance = global_context (request))

def display_supercoord_portal (request, supercoord):
    """
    Display supercoord's portal
    """
    display_dict = dict ()

    if request.method == "POST":
        if 'delete' in request.POST:
            delete_tasks=request.POST.getlist('delete_tasks')
            for i in delete_tasks:
                deltask=Task.objects.get(pk=i)
                for delcomment in deltask.taskcomment_set.all():
                    delcomment.delete()
                for delsubtask in deltask.subtask_set.all():
                    for delsubtaskcomment in delsubtask.subtaskcomment_set.all():
                        delsubtaskcomment.delete()
                    delsubtask.delete()
                deltask.delete()
            display_dict['tasks_deleted'] = True
                
    # Deal with the Updates part (viewing, creating) of the portal
    update_dict = handle_updates (request, supercoord)
    department = supercoord.get_profile ().department
    display_dict['group'] = supercoord.groups.all()[0]
    display_dict['all_Tasks'] = get_timeline (supercoord)
    display_dict['all_SubTasks'] = get_subtasks (supercoord)
    display_dict['all_completed_SubTasks'] = get_completed_subtasks (supercoord)
    
    
    #Get Department Members' image thumbnails
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_supercoords_list'] = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
        
    qms_supercoord=False
    curr_userprofile=userprofile.objects.get(user=request.user)
    if str(department) == 'QMS':
		display_dict['qms_supercoord']=True
    
    # Include the key-value pairs in update_dict
    display_dict.update (update_dict)
    return render_to_response('tasks/supercoord_portal.html',
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
    
    #Get Department Members' image thumbnails
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_supercoords_list'] = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    if str(department) == 'QMS':
		display_dict['qms_coord']=True
        
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
    if(curr_task.status=='C'):
        closed_task=1                     # The SubTask Was closed prior to editing
    else:
        closed_task=0                     # The SubTask is not closed prior to editing


    # curr_object = Task.objects.get (id = task_id)
    is_task_comment = True
    other_errors = False

    #Get all subtasks for task, if task exists
    if task_id:
        curr_subtasks = SubTask.objects.filter(task = curr_task)
        
    #Get Department Members' image thumbnails
    display_dict = dict ()
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    SubTaskFormSet = inlineformset_factory (Task,
                                            SubTask,
                                            form = SubTaskForm,
                                            exclude = subtask_exclusion_tuple,
                                            extra = 0,
                                            can_delete = True)

    SubTaskFormSet.form = staticmethod(curry(SubTaskForm, editor=request.user))
                                           
    if request.method == 'POST':
        # Get the submitted formset
        subtaskfs = SubTaskFormSet (request.POST,
                                    instance = curr_task)
        template_form = subtaskfs.empty_form
        task_form = TaskForm (request.POST, instance = curr_task)
        if task_form.is_valid () and subtaskfs.is_valid ():
            curr_task = task_form.save (commit = False)
            
            if(curr_task.status=='C')and(closed_task == 0):
                curr_task.completion_date=datetime.date.today()                    
            elif(closed_task == 1):
                curr_task.completion_date=None
            curr_task.save()
            print 'Task : ', curr_task

#            comments, comment_form, comment_status = handle_comment (
#                request = request,
#                is_task_comment = True,
#                object_id = task_id)

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
                #subtask.department=request.user.get_profile().department
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
        print "atleast here" 
    
    curr_userprofile=userprofile.objects.get(user=user)
    if is_core(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_core= True

    if is_supercoord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True

    if is_coord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_coord= True

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
    curr_subtask_form = SubTaskForm (instance = curr_subtask,editor=request.user)

    if curr_subtask.is_owner (user):
        is_owner = True
    else:
        # User is a Coord
        is_owner = False

    if(curr_subtask.status=='C'):
        closed_task=1                     # The SubTask Was closed prior to editing
    else:
        closed_task=0                     # The SubTask is not closed prior to editing
    has_updated = False
    other_errors = False

    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department          
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    if request.method == 'POST':
        if is_owner:
            # Let the Core save the SubTask
            curr_subtask_form = SubTaskForm (request.POST, instance = curr_subtask)
            if curr_subtask_form.is_valid ():
                if 'status' in request.POST:                
                    if(curr_subtask_form.cleaned_data['status']=='C')and(closed_task == 0):
                        curr_subtask_form.completion_date=datetime.date.today()                    
                    elif(closed_task == 1):
                        curr_subtask_form.completion_date=None
                curr_subtask_form.save ()
                has_updated = True
            else:
                other_errors = True
        elif 'status' in request.POST:
            # Coord - allowed to change only the status
            curr_subtask.status = request.POST.get ('status', 'O') 
            if(curr_subtask.status=='C')and(closed_task == 0):
                curr_subtask.completion_date=datetime.date.today()                    
            elif(closed_task == 1):
                curr_subtask.completion_date=None
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
    
    curr_userprofile=userprofile.objects.get(user=user)
    if is_core(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_core= True

    if is_supercoord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True
            
    if is_coord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_coord= True     

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

    curr_userprofile=userprofile.objects.get(user=user)
    if is_core(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_core= True

    if is_supercoord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True

    if is_coord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_coord= True

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
    user = request.user
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department          
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    print 'Display Task - Task ID : ', task_id
    curr_task = Task.objects.get (id = task_id)
    comments = TaskComment.objects.filter (task__id = task_id)

    curr_userprofile=userprofile.objects.get(user=user)
    if is_core(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_core= True

    if is_supercoord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True
            
    if is_coord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_coord= True

    return render_to_response('tasks/display_task.html',
                              locals(),
                              context_instance = global_context (request))



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
        if page_owner.groups.filter (name = 'Supercoords'):
            # For Supercoords
            update_form = UpdateForm ()
            update_status = "Blank"
            update_dict['updates'] = get_all_updates (page_owner.get_profile ().department)
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
    display_dict['shouts']=shouts
    display_dict['shout_form']=shout_form
    display_dict['all_Tasks'] = get_timeline (page_owner)
    display_dict['updates'] = get_all_updates (department)
    
    #Get Department Members' image thumbnails
    display_dict ['dept_cores_list'] = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    display_dict ['dept_supercoords_list'] = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    display_dict ['dept_coords_list'] = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    qms_core=False
    if is_core(request.user):
		if str(department) == 'QMS':
			display_dict['qms_core']=True

    qms_supercoord = False
    if is_supercoord(request.user):
        if str(department) == 'QMS':
            display_dict['qms_supercoord']= True
            
    qms_coord=False
    if is_coord(request.user):
		if str(department) == 'QMS':
			display_dict['qms_coord']=True

    return render_to_response('tasks/department_portal.html',
                              display_dict,
                              context_instance = global_context (request))


def remainder(request):
    """
        Here we check if the user is a coord. 
        Then we get all the subtasks assigned to the coord which are only 3 days away from overdue. 
        If it is the case we send them a mail, stating the subject of the subtask which is not yet completed and only 3 days from overdue along with its deadline and status
        This is automated using cron and calling the respective url of this view everday.
    """
    users=userprofile.objects.all()
    t=get_template('mail_template.html')
    today=date.today()
    datatuple=()
    for user1 in users:
        if is_coord(user1.user):
            subtasks=SubTask.objects.filter(coords=user1.user).filter(deadline=today+relativedelta(days=+3))
            if subtasks:
                work_pending=False
                for subtask in subtasks:
                    if subtask.status != 'C':
                        work_pending=True
                if work_pending:
                    body=t.render(Context({'name':user1.user.username ,'subtasks':subtasks}))
                    msg=EmailMessage('Remainder',body,'noreply@shaastra.org',[user1.user.email])
                    msg.content_subtype="html"
                    datatuple+= (
                    (msg),
                    )
    connection=mail.get_connection()
    connection.send_messages(datatuple)
    return HttpResponse("remainder sent!")
