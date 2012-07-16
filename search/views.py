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
    return render_to_response('search/search.html', locals(),RequestContext(request))
            
    
     
    
            

        
    
