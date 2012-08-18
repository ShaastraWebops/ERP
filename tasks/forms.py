from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from erp.department.models import *
from erp.users.models import *
from django.contrib.auth.models import User
#from chosen import widgets as chosenwidgets

class TaskCommentForm (ModelForm):
	comment_string=forms.CharField(label='Comments',widget=forms.Textarea)
	class Meta:
		model=TaskComment
		exclude=('author','task')	

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
        model = Task
        exclude = ('creator', )
        widgets = {'status': chosenforms.widgets.ChosenSelect()}

class SubTaskForm (ModelForm):
    class Meta:
        model = SubTask
        exclude = ['creator', 'description', 'department', 'task']
        widgets = {'department':chosenforms.widgets.ChosenSelect(),'coords': chosenforms.widgets.ChosenSelectMultiple(),'status': chosenforms.widgets.ChosenSelect()}
    
    def __init__(self, user=None, *args, **kwargs):
        super(SubTaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['coords'].queryset = User.objects.filter(userprofile__department=user.get_profile().department)
            self.fields['coords'].help_text = ''
        
#hack if these fields need to be formatted        
#    def __init__(self, *args, **kwargs):
#        super(SubTaskForm, self).__init__(*args, **kwargs)
#        self.fields['subject'].widget.attrs['rows'] = '500'
#        self.fields['subject'].widget.attrs['cols'] = '500'
        
