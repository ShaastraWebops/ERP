from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
class TaskCommentForm (ModelForm):
    class Meta:
        model = TaskComment
        exclude = ('author', 'task')

class SubTaskCommentForm (ModelForm):
    class Meta:
        model = SubTaskComment
        exclude = ('author', 'subtask')                

class UpdateForm (ModelForm):
    class Meta:
        model = Update
        exclude = ('author')

class TaskForm (ModelForm):
    class Meta:
        widgets={'deadline':forms.TextInput(attrs={'id':'popupDatepicker'}) ,}
        model = Task
        exclude = ('creator', )

class SubTaskForm (ModelForm):
    class Meta:
        widgets={'deadline':forms.TextInput(attrs={'id':'popupDatepicker'}) ,}
        model = SubTask
        exclude = ('creator', 'description', 'department', 'task')
