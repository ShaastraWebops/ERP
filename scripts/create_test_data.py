# Helper functions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.db.models import Q
from erp import settings
from erp.users import models
from erp.department.models import Department, DEP_CHOICES
from erp.tasks.models import Task, SubTask, DEFAULT_STATUS, TaskComment, SubTaskComment, Update
import random ,datetime

def create_group (group_name):
    """
    Create a group with group_name, if it doesn't already exist.
    """
    try:
        new_group = Group.objects.get (name = group_name)
    except:
        new_group = Group (name = group_name)
        new_group.save ()
        print 'Group %s created' %(group_name)

def create_groups ():
    """
    Create groups Cores, Coords, and Vols (if they don't already exist).
    """
    group_list = ['Cores', 'Coords', 'Vols',]
    for group_name in group_list:
        create_group (group_name)

def create_depts ():
    """
    Create all the departments with names as given DEP_CHOICES.
    """
    for name, description in DEP_CHOICES:
        try:
            dept = Department.objects.get (Dept_Name = name)
            print 'Department %s exists' %(name)
        except:
            new_dept = Department.objects.create (Dept_Name = name)
            print 'Department %s created' %(name)

def add_user_to_group (user, group_name):
    # Allow access to admin interface
    if group_name == 'Cores':
        user.is_staff = True
    else:
        user.is_staff = False
    user.groups.add (Group.objects.get (name = group_name))
    user.save ()
    print '%s - now a member of Group %s' %(user, group_name)

def create_user (department_name, group_name, user_dict, profile_dict):
    """
    Create a User and fill his userprofile.
    """
    try:
        # In case, user already exists
        user = User.objects.get (username = user_dict['username'])
        print '%s - User exists' %(user_dict['username'])
    except:
        # If it's a new user
        # Note : create_user creates an instance and saves it in the database
        # Delivering keyword args in user_dict
        user = User.objects.create_user(**user_dict)
        print '%s - User created' %(user_dict['username'])
    try:
        curr_userprofile = user.get_profile ()
        print "%s - userprofile exists" %(user_dict['username'])
    except:
        # If userprofile doesn't exist (whether or not user is a new
        # one or old one), create it
        profile_dict['user'] = user
        profile_dict['department'] = Department.objects.get (Dept_Name = department_name)
        curr_userprofile = models.userprofile (**profile_dict)
        curr_userprofile.save ()
        print "%s - userprofile created" %(user_dict['username'])
    add_user_to_group (user, group_name)

def parse_user_info_list (info_list):
    """
    Parse given line into appropriate data and return a list of department_name, group_name, and two dicts :
    user_dict - which contains user info
      - username
      - email
      - password
    profile_dict - which contains userprofile info
      - nickname
      - name
      - chennai_number
      - summer_number
      - summer_stay
      - hostel
      - room_no
    """
    department_name = info_list[0]
    group_name = info_list[1]
    user_keys = ['username', 'email', 'password']
    profile_keys = ['nickname', 'name', 'chennai_number', 'summer_number', 'summer_stay', 'hostel', 'room_no']
    user_values = info_list[2:5]
    profile_values = info_list[5:]
    user_dict = dict (zip (user_keys, user_values))
    profile_dict = dict (zip (profile_keys, profile_values))
    return [department_name, group_name, user_dict, profile_dict]

def create_users (users_file_name = 'users.txt'):
    """
    Get user details from users_file_name.
    Create users if they doesn't exist.
    """
    users_file = open (users_file_name, 'r')
    for line in users_file:
        # user_fields = line.split ()
        user_data_list = parse_user_info_list (line.split ())
        create_user (*user_data_list)
    users_file.close ()
    print 'All users created successfully.'

# def create_task (task_details, subtask_list = None):
#     """
#     Arguments:
#     - `task_details`:
#     - `subtask_list`:
#     """
#     task_keys = ["subject", "description", "creator", "deadline"]
#     subtask_keys = ["subject", "description", "creator", "deadline"]

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
        subtask_subj_str_same = ' Same Dept - Do this (Partial)'
        subtask_subj_str_other = ' Other Dept - Do this (Partial)'
    else:
        num_other_tasks = 1
        task_subj_str = ' Test Task '
        subtask_subj_str_same = ' Same Dept - Do this '
        subtask_subj_str_other = ' Other Dept - Do this '
    for name in dept_names:
        curr_dept = Department.objects.get (Dept_Name = name)
        # This Department's Core
        curr_core = User.objects.filter (groups__name = 'Cores', userprofile__department__Dept_Name = name)[0]
        curr_coord1 = User.objects.filter (groups__name = 'Coords', userprofile__department__Dept_Name = name)[0]
        curr_coord2 = User.objects.filter (groups__name = 'Coords', userprofile__department__Dept_Name = name)[1]
        print 'Tasks for ', curr_dept.Dept_Name
    start_date = datetime.date.today().replace(day=1, month=7).toordinal()
    end_date = datetime.date.today().toordinal()
    print start_date
    print end_date
    for i in xrange (n):
        new_task = Task ()
        new_task.subject = name + task_subj_str + str (i)
        new_task.description = 'Gen Testing ' + str (i)
        new_task.creator = curr_core
        new_task.deadline =  datetime.date.fromordinal(random.randint(0,9))#changed
        new_task.save () 
        if not partial_subtask:
            subtask1 = SubTask ()
            subtask1.subject = name + subtask_subj_str_same + str (i)
            subtask1.creator = curr_core
            subtask1.deadline =  datetime.date.fromordinal(random.randint(start_date, end_date))
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
            subtask2.deadline =  datetime.date.fromordinal(random.randint(start_date, end_date))
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
            print 'Task ', i, 'Created'

def finish_some_subtasks ():
    """
    Mark one complete SubTask in each Department as Done.
    """
    dept_names = [tup[0] for tup in DEP_CHOICES]
    print 'Subtasks marked as completed :'
    for name in dept_names:
        # The SubTask must not be a partial SubTask (for the sake of testing)
        try:
            curr_subtask = SubTask.objects.filter (~Q (coords = None), department__Dept_Name = name)[0]
            curr_subtask.status = 'C'
            print curr_subtask
            curr_subtask.save ()
        except:
            pass

def create_comments ():
    """
    Create some comments for each Task, SubTask.
    """
    cores_list = User.objects.filter (groups__name = 'Cores')
    coords_list = User.objects.filter (groups__name = 'Coords')
    standard_test_comment = ' Testing 123'
    for core in cores_list:
        task_list = Task.objects.filter (creator = core)
        subtask_list = SubTask.objects.filter (department = core.get_profile ().department)
        comment_string = core.get_profile ().name + ' '
        for task in task_list:
            new_comment = TaskComment (comment_string = comment_string + 'Task' + standard_test_comment)
            new_comment.author = core
            new_comment.task = task
            new_comment.save ()
        for subtask in subtask_list:
            new_comment = SubTaskComment (comment_string = comment_string + 'SubTask' + standard_test_comment)
            new_comment.author = core
            new_comment.subtask = subtask
            new_comment.save ()
    print 'Core comments - Created'
    for coord in coords_list:
        # List of all SubTasks where coord is one of the Coords assigned
        subtask_list = SubTask.objects.filter (coords = coord)
        comment_string = coord.get_profile ().name + ' '
        for subtask in subtask_list:
            new_comment = SubTaskComment (comment_string = comment_string + 'SubTask' + standard_test_comment)
            new_comment.author = coord
            new_comment.subtask = subtask
            new_comment.save ()
    print 'Coord comments - Created'

def create_updates ():
    """
    Create some updates for each Coord.
    """
    coords_list = User.objects.filter (groups__name = 'Coords')
    for coord in coords_list:
        # List of all SubTasks where coord is one of the Coords assigned
        new_update = Update (comment_string = 'Hey This is Me ' + coord.get_profile ().name, author = coord)
        new_update.save ()
        new_update = Update (comment_string = 'Yo! This is Me again! ' + coord.get_profile ().name, author = coord)
        new_update.save ()
        new_update = Update (comment_string = 'Guess What? ' + coord.get_profile ().name, author = coord)
        new_update.save ()
    print 'Coord updates - Created'

# Create Core
# create_test_data.create_user ('Webops', 'Cores', {'username' : 'me09b001', 'email' : '', 'password' : 'password'}, {'nickname' : 'IBM', 'name' : 'Siddharth', 'chennai_number' : '9999999999', 'summer_number' : '9999999999', 'summer_stay' : 'Bangalore', 'hostel' : 'Godavari', 'room_no' : '420'})

def do_it_all ():
    create_groups ()
    create_depts ()
    create_users (users_file_name = '/home/sriram/Django/erp/scripts/users.txt')
    create_tasks (n = 5, partial_subtask = False)
    create_tasks (n = 3, partial_subtask = True)
    finish_some_subtasks ()
    create_updates ()
    create_comments ()


