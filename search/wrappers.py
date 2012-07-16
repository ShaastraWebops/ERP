from haystack.query import *
from erp.tasks.models import *
from erp.users.models import *
from erp.misc.util import *
from erp.misc.helper import *


def handle_search(request,search_term):
    if not is_core(request.user):
        search_results = SearchQuerySet()
        print get_department(request)
        tasks = search_results.filter(content = search_term).models(Task)
        users = search_results.filter(content = search_term).models(userprofile)
        subtasks = search_results.filter(content = search_term).filter(department = get_department(request)).models(SubTask)
        
    results = {'tasks':tasks, 'users':users, 'subtasks':subtasks }
    return results
    
def spelling(search_term):

    return SearchQuerySet().spelling_suggestion(search_term)
