from django.db import models
from django.forms import ModelForm
from models import *

class TaskCommentForm (ModelForm):
    class Meta:
        model = TaskComment
        exclude = ('author', 'task')

class SubTaskCommentForm (ModelForm):
    class Meta:
        model = SubTaskComment
        exclude = ('author', 'subtask')                

class TaskForm (ModelForm):
    class Meta:
        model = Task
        exclude = ('creator', )

class SubTaskForm (ModelForm):
    class Meta:
        model = SubTask
        exclude = ('creator', 'description', 'department', 'task')
        
class UpdatesForm (ModelForm):
    class Meta:
        model = Updates
        exclude = ('coord')
