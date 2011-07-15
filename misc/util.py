# Helper functions
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from erp.users.models import *

from erp import settings
from erp.users import models
from erp.department.models import Department
import os # upload files
import MySQLdb
import re, md5, time

# Some macros for readability
NORMAL = 1
FILE = 2
MCQ = 3
MESSAGE = 4

# Generates a context with the most used variables
def global_context(request):
    # The try...except blocks are there for the case when an anonymous
    # user visits any page (esp the login page)
    try:
        user_dept_name = request.user.get_profile ().department.Dept_Name
    except:
        user_dept_name = False
    try:
        user_name = request.user.get_profile ().name
    except:
        user_name = False

    try:
        photo_list=userphoto.objects.filter()           
    except:
        photo_list=False    

    page_owner = request.session.get ('page_owner', request.user)
    print "this is the page owner (form util.py ) ",page_owner

    try:
        po_dept_name = page_owner.get_profile ().department.Dept_Name
    except:
        po_dept_name = False

    try:
        po_name = page_owner.get_profile ().name
    except:
        po_name = False

    if page_owner != request.user:
        is_visitor = True
    else:
        is_visitor = False

    context =  RequestContext (request,
            {'user':request.user,
            'SITE_URL':settings.SITE_URL,
             'user_dept_name': user_dept_name,
             'user_name': user_name,
             'is_core' : is_core (request.user),
             'is_coord' : not is_core (request.user),
             'po_is_core' : is_core (page_owner),
             'po_is_coord' : not is_core (page_owner),
             'is_visitor' : is_visitor,
             'page_owner' : page_owner,
             'po_name' : po_name,
             'po_dept_name' : po_dept_name,
             'photo_list':photo_list,

            })
    return context

# Error pages
def not_found (request):
    return render_to_response('404.html', locals(), context_instance= global_context(request)) 
def server_error (request):
    return render_to_response('500.html', locals(), context_instance= global_context(request)) 


# Convert Foo Contest <-> FooContest
def camelize (str):
    return str.replace (' ','')
def decamelize (str):
    p = re.compile (r'([A-Z][a-z]*)')
    result = ''
    for blob in p.split (str):
        if blob != '':
            result += blob + ' '
    return result[:-1]

# Take care of session variable
# Note : This will pop the key from request.session
def session_get (request, key, default=False):
    value = request.session.get (key, False)
    if value:
        pass
        del request.session[key]
    else: 
        value = default
    return value


# Decorators

# Force authentication first
def needs_authentication (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if not request.user.is_authenticated():
            # Return here after logging in
            request.session['from_url'] = request.path
            
            print "path from util", request.path
            return HttpResponseRedirect ("%s/home/login/"%settings.SITE_URL)
        else:
            return func (*__args, **__kwargs)
    return wrapper


# For urls that can't be accessed once logged in.
def no_login (func):
    def wrapper (*__args, **__kwargs):
        request = __args[0]
        if request.user.is_authenticated():
            # Return here after logging in
            request.session['already_logged'] = True
	    #html = "%s/home/" %SITEURL
            return HttpResponseRedirect ("%s/home/" %settings.SITE_URL)
        else:
            return func (*__args, **__kwargs)
    return wrapper

# TODO : decorator
# def page_owner_only (redirect_url = None):
#     """
#     If user is not of the same department as the task, then just
#     display the task, etc.
#     """
#     def _dec(func):
#         def wrapper (*__args, **__kwargs):
#             request = __args[0]
#             if not request.user.is_authenticated():
#                 # Return here after logging in
#                 request.session['from_url'] = request.path
#                 return HttpResponseRedirect ("%s/home/login/"%settings.SITE_URL)
#             else:
#                 return func (*__args, **__kwargs)
#         return wrapper
#     return _dec


# Temporary workaround for the fact that I don't know whether / how to
# extend the User class with methods
def is_core (user):
    """
    Return True if user is a Core.
    """
    try:
        if user.groups.filter (name = 'Cores'):
            return True
    except:
        return False




"""
this function creates the directory which will store infromation about the user
like his photos , documents

"""

def create_dir(file_name ,user_name , method=1):
    destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
    destdir=os.path.join(destdir_one,user_name)
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
    save_path=os.path.join(destdir,os.path.basename(file_name))
            
    destdir_one=os.path.join(settings.MEDIA_URL,"upload_files")
    destdir=os.path.join(destdir_one,user_name)
    print destdir , "is the destdir for the file"
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
    file_path=os.path.join(destdir,os.path.basename(file_name))
    
    return (save_path , file_path)



"""
this function writes the file
takes a file and saves it in recpective path


"""

def write_file(save_path ,f ,method=1):
    fout=open(save_path,'wb+')
    for chunk in f.chunks():
        fout.write(chunk)
    fout.close()


def get_page_owner (request, owner_name):
    """
    If owner_name is passed, return page owner, if he exists. If user
    with that name doesn't exist, return 'Invalid'.

    Else, return current user.

    Also, set the session variable for page_owner.
    """
    print 'Get Page Owner - owner_name : ', owner_name
    if owner_name == '' or owner_name is None:
        page_owner = request.user
    else:
        try:
            page_owner = User.objects.get (username = owner_name)
        except:
            return 'Invalid'
    request.session['page_owner'] = page_owner
    return page_owner

