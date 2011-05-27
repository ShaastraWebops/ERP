# Helper functions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.db.models import Q

from erp import settings
from erp.users import models
from erp.department.models import Department, DEP_CHOICES
from erp.tasks.models import Task, SubTask, DEFAULT_STATUS
import random

def create_groups ():
    cores = Group (name = 'Cores')
    cores.save ()
    coords = Group (name = 'Coords')
    coords.save ()
    vols = Group (name = 'Vols')
    vols.save ()

def create_depts ():
    for name, description in DEP_CHOICES:
        try:
            new_dept = Department.objects.create (Dept_Name = name, Event_Manager = User.objects.get (username = 'root'))
        except:
            pass
    

def create_users (users_file_name):
    """
    Get user details from users_file_name. Create user if it doesn't exist, update  user if it already exists.
    Record Format:
    department username email password first_name last_name mobile_number group
    """
    users_file = open (users_file_name, 'r')
    for line in users_file:
        # user_fields = line.split ()
        department, username, email, password, first_name, last_name, mobile_number, group = line.split ()
        print department, username, email, password, first_name, last_name, mobile_number, group  
        try:
            # In case, user already exists
            user = User.objects.get (username = username)
        except:
            user = User.objects.create_user(username = username, password = password, email = '')
        if group == 'Cores':
            user.is_staff = True
            if user.groups.filter (name = 'Coords'):
                user.groups.remove (Group.objects.get (name = 'Coords'))
        else:
            user.is_staff = False
        user.groups.add (Group.objects.get (name = group))

        try:
            # See if a userprofile exists
            curr_userprofile = user.userprofile_set.all ()[0]
            curr_userprofile.first_name, curr_userprofile.last_name, curr_userprofile.mobile_number = first_name, last_name, mobile_number
            curr_userprofile.department = Department.objects.get (Dept_Name = department)
            curr_userprofile.save ()
        except:
            # If no userprofile exists for this User
            new_userprofile = models.userprofile ()
            new_userprofile.user = user
            new_userprofile.first_name, new_userprofile.last_name, new_userprofile.mobile_number = first_name, last_name, mobile_number
            new_userprofile.department = Department.objects.get (Dept_Name = department)
            new_userprofile.save ()
        user.save ()
    users_file.close ()

def create_tasks (n = 5, partial_subtask = False):
    """
    Create n (= 5) Tasks (with 2 SubTasks each) for each Department's
    Core, with Deadline as 15 June, 2011. One SubTask is for the
    Core's Department. The other is for a random Department.

    If partial_subtask = True, mark both SubTasks for other
    Departments (at random), but don't assign to their Coords.
    """
    
    dept_names = [tup[0] for tup in DEP_CHOICES]
    if partial_subtask:
        num_other_tasks = 2
        task_subj_str = ' Test Task (Partial) '
        subtask_subj_str_same = 'Same Dept - Do this (Partial)'
        subtask_subj_str_other = 'Other Dept - Do this (Partial)'
    else:
        num_other_tasks = 1
        task_subj_str = ' Test Task '
        subtask_subj_str_same = 'Same Dept - Do this'
        subtask_subj_str_other = 'Other Dept - Do this'


    for name in dept_names:
        curr_dept = Department.objects.get (Dept_Name = name)
        # This Department's Core
        curr_core = User.objects.filter (groups__name = 'Cores', userprofile__department__Dept_Name = name)[0]
        curr_coord1 = User.objects.filter (groups__name = 'Coords', userprofile__department__Dept_Name = name)[0]
        curr_coord2 = User.objects.filter (groups__name = 'Coords', userprofile__department__Dept_Name = name)[1]
        print curr_dept.Dept_Name
        for i in xrange (n):
            new_task = Task ()
            new_task.subject = name + task_subj_str + str (i)
            new_task.description = 'Gen Testing ' + str (i)
            new_task.creator = curr_core
            new_task.deadline = '2011-06-15'
            new_task.save () 

            if not partial_subtask:
                subtask1 = SubTask ()
                subtask1.subject = name + subtask_subj_str_same + str (i)
                subtask1.creator = curr_core
                subtask1.deadline = '2011-06-10'
                subtask1.department = curr_dept
                subtask1.task = new_task
                # Seems the SubTask must exist before many to many
                # relations can be added
                subtask1.save ()
                subtask1.coords.add (curr_coord1)
                subtask1.coords.add (curr_coord2)
                subtask1.save ()

            for j in xrange (num_other_tasks):
                subtask2 = SubTask ()
                subtask2.creator = curr_core
                subtask2.deadline = '2011-06-10'
                index = random.randint (0, 9)
                subtask2.department = Department.objects.get (Dept_Name = dept_names[index])
                subtask2.subject = subtask2.department.Dept_Name + subtask_subj_str_other + str (i)
                subtask2.task = new_task
                # Seems the SubTask must exist before many to many
                # relations can be added
                subtask2.save ()
                if not partial_subtask:
                    # If not a partial subtask, assign to coords
                    coord_list = User.objects.filter (groups__name = 'Coords', userprofile__department__Dept_Name = dept_names[index])
                    subtask2.coords.add (coord_list[0])
                    subtask2.coords.add (coord_list[1])
                    subtask2.save ()
                print i, 'Done'


def finish_some_subtasks ():
    """
    Mark one complete SubTask in each Department as Done.
    """
    dept_names = [tup[0] for tup in DEP_CHOICES]
    for name in dept_names:
        # The SubTask must not be a partial SubTask (for the sake of testing)
        try:
            curr_subtask = SubTask.objects.filter (~Q (coords = None), department__Dept_Name = name)[0]
            curr_subtask.status = 'C'
            print curr_subtask
            curr_subtask.save ()
        except:
            pass
    

