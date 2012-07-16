from haystack.query import *
from erp.tasks.models import *
from erp.users.models import *


def handle_search(request,search_term):
    search_results = SearchQuerySet()
    tasks = search_results.filter(content = search_term).models(Task)
    users = search_results.filter(content = search_term).models(userprofile)
    subtasks = search_results.filter(content = search_term).models(SubTask)
    
    results = {'tasks':tasks, 'users':users, 'subtasks':subtasks }
    return results
    
def spelling(search_term):

    return SearchQuerySet().spelling_suggestion(search_term)
