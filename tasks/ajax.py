from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from models import *
from forms import *
from erp.dashboard.models import *
from erp.misc.helper import *
from erp.misc.util import *
from erp.tasks.render import *
from django.template import Template, Context
from django.template.loader import get_template
import datetime
from django.core.context_processors import request


@dajaxice_register
def shout(request, shout=None):
    print request.user, 'just shouted', shout, 'at', datetime.datetime.now()
    dajax=Dajax()
    if shout is not None:
        new_shout=add_shout(request, shout)
    shouts = shout_box.objects.all()
    template = get_template('tasks/shoutbox.html')  
    html = template.render(Context({'shouts':shouts}))
    dajax.assign('#markup','innerHTML', html)
    dajax.assign('#shout_button','innerHTML', 'Shout!')
    return dajax.json()
          
    
def add_shout(request,shout):
    new_shout=shout_box()   
    new_shout.user = request.user
    new_shout.nickname = request.user.get_profile().nickname
    new_shout.comments = shout
    new_shout.timestamp = datetime.datetime.now()
    new_shout.save()
    print 'saved', new_shout 
    
@dajaxice_register
def comment(request, object_id=None, comment=None, is_task=True, elementid=None):
    print "Comment at", object_id, 'Comment', comment, 'Is task', is_task, 'ELEM', elementid
    dajax = Dajax()
    if is_task=='True':
        task_id = object_id
        add_task_comment(request, task_id, comment)
        comments = TaskComment.objects.filter(task__id = task_id)
        template = get_template('tasks/comments/task_comment_table.html')
    else:
        subtask_id = object_id
        add_subtask_comment(request, subtask_id, comment)
        comments = SubTaskComment.objects.filter(subtask__id = subtask_id)
        template = get_template('tasks/comments/subtask_comment_table.html')
    
    html = template.render(Context({'comments':comments}))  
    dajax.assign(elementid, 'innerHTML', html)
    return dajax.json()
   
def add_task_comment(request, task_id, comment):
    
    taskcomment = TaskComment()
    taskcomment.task = Task.objects.filter(id = task_id)[0]    
    taskcomment.author = request.user
    taskcomment.comment_string = comment
    taskcomment.time_stamp = datetime.datetime.now()
    taskcomment.save()
    print 'saved', taskcomment

def add_subtask_comment(request, subtask_id, comment):
    subtaskcomment = SubTaskComment()
    subtaskcomment.subtask = SubTask.objects.filter(id = subtask_id)[0]    
    subtaskcomment.author = request.user
    subtaskcomment.comment_string = comment
    subtaskcomment.time_stamp = datetime.datetime.now()
    subtaskcomment.save()
    print 'saved', subtaskcomment.comment_string


# This was the Previous addcomment handler. Delete when cleaning code. Currently present so that Subtask Comments dont throw an exception
# TODO: Subtask Comments

def handle_comment (request, is_task_comment, object_id, other_errors = False):
    """
    Return a tuple : (comments, comment form, status).

    comments : Comments for that object, if it exists. Else, None.
    other_errors : Whether the rest of the Task / SubTask form has
    errors. In that case, just keep the comment form content as is.

    If the form was POSTed, then save the comment and return comments,
    empty form, status = 'Success'.

    If the form data is invalid (ie. if it is blank) or if
    other_errors is True, then return status as 'Error'

    Else, return blank form and status = 'Blank'

    If is_task_comment is True, treat it as a TaskComment.
    Else, treat it as a SubTaskComment.
    """    
    success = False
    not_found = True
    user = request.user


    if is_task_comment:
        curr_modelform = TaskCommentForm
        curr_model = Task
        comments = TaskComment.objects.filter (task__id = object_id)
    else:
        curr_modelform = SubTaskCommentForm
        curr_model = SubTask
        comments = SubTaskComment.objects.filter (subtask__id = object_id)

    if request.method == 'POST':
        comment_form = curr_modelform (request.POST)            
        if not other_errors and comment_form.is_valid():
            new_comment = comment_form.save (commit = False)
            curr_object = curr_model.objects.get (id = object_id)
            success = True
            new_comment.author = user
            if is_task_comment:
                new_comment.task = curr_object
            else:
                new_comment.subtask = curr_object
            new_comment.save ()
            # Blank the form
            comment_form = curr_modelform ()
            return (comments, comment_form, 'Success')
        else:
            return (comments, comment_form, 'Error')
    else:
        comment_form = curr_modelform ()
    return (comments, comment_form, 'Blank')
        
