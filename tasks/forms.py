from django.db import models
from django.forms import ModelForm
from models import *

class TaskCommentForm (ModelForm):
    class Meta:
        model = TaskComment

class SubTaskCommentForm (ModelForm):
    class Meta:
        model = SubTaskComment

class TaskForm (ModelForm):
    class Meta:
        model = Task

class SubTaskForm (ModelForm):
    class Meta:
        model = SubTask
