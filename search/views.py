# Create your views here.

from haystack.query import *
from erp.tasks.models import *
from erp.users.models import *
from erp.search.wrappers import *
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
import urllib
from django.template.context import Context, RequestContext
from erp.misc.helper import is_core, is_coord, get_page_owner
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from erp.misc.util import *


@login_required(login_url='/erp/', redirect_field_name=None)
def search(request, search_term=None):  
    print request.method
    page_owner = get_page_owner (request, None)                               
    if request.method == "POST":
        query = request.POST['searchbar']
        search_term = '/search/'+str(urllib.urlencode({'':query}))
        print search_term
        return HttpResponseRedirect(search_term)         
    if not search_term:
            return render_to_response('search/search.html', locals(),RequestContext(request))     
    results = handle_search(request,search_term)
    if spelling(search_term) is not '':
        spelling_suggestion = spelling(search_term)
    tasks = results['tasks']
    users = results['users']
    subtasks = results['subtasks']
    
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

    return render_to_response('search/search.html', locals(),RequestContext(request))
            
    
     
    
            

        
    
