# Helper functions
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template.context import Context, RequestContext

from erp import settings
from erp.users import models
from erp.department.models import Department

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
        user_dept_name = request.user.userprofile_set.all()[0].department.Dept_Name
    except:
        user_dept_name = False
    try:
        core_group = request.user.groups.filter (name = 'Cores')
        coord_group = request.user.groups.filter (name = 'Coords')
    except:
        coord_group = False
        core_group = False

    page_owner = request.session.get ('page_owner', request.user)
    try:
        po_core_group = page_owner.groups.filter (name = 'Cores')
        po_coord_group = page_owner.groups.filter (name = 'Coords')
    except:
        po_coord_group = False
        po_core_group = False
    try:
        page_owner_dept_name = page_owner.get_profile ().department.Dept_Name
    except:
        page_owner_dept_name = False
    context =  RequestContext (request,
            {'user':request.user,
            'SITE_URL':settings.SITE_URL,
             'user_dept_name': user_dept_name,
             'is_core' : core_group,
             'is_coord' : coord_group,
             'po_is_core' : po_core_group,
             'po_is_coord' : po_coord_group,
             'is_visitor' : request.session.get ('is_visitor', False),
             'page_owner' : page_owner,
             'page_owner_dept_name' : page_owner_dept_name,
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
# def same_dept_only (redirect_url = None):
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
