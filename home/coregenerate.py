import csv
from users.models import *
from django.contrib.auth.models import User, Group
from department.models import *
from django.shortcuts import HttpResponseRedirect
import string
import random
from time import sleep
from erp.dashboard.create_test_data import create_group, create_user, parse_user_info_list, create_depts

OUT_FILE="home/coredetailsdone.csv"

def supercoreAssociations (users_file_name = 'coredetailsdone.csv'):
    supercore = None
    details=csv.reader(open(users_file_name, 'rb'))
    line=details.next()
    def addDept(line):
        if '_' in line[2]:
            dept = Department.objects.get(Dept_Name = line[0])
            supercorename = line[2].split('_')[0]
            supercore = User.objects.get(username = supercorename)
            dept.owner.add(supercore)
            dept.save()
            print dept, "is now associated with", supercore
        try:
            line=details.next()
            addDept(line)
        except:
            pass             
    return addDept(line)

def create_users (users_file_name = 'coredetailsdone.csv'):
    """
    Get user details from users_file_name.
    Create users if they doesn't exist.
    """
    users_file = open (users_file_name, 'r')
    for line in users_file:
        # user_fields = line.split ()
        user_data_list = parse_user_info_list (line.split (','))
        print user_data_list
        create_user (*user_data_list)
    users_file.close ()
    print 'All users created successfully.'

def write_into_db(request):    
    # Create group if already not there
    create_group('Cores')
    create_depts ()
    create_users (users_file_name = OUT_FILE)
    supercoreAssociations (users_file_name = OUT_FILE)
    return HttpResponseRedirect('/')
