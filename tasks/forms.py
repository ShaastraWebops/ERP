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
        exclude = ('creator', 'completion_date')
        widgets = {'status': chosenforms.widgets.ChosenSelect()}

class SubTaskForm (ModelForm):
    class Meta:
        model = SubTask
        exclude = ['creator', 'task', 'completion_date']
        widgets = {'department':chosenforms.widgets.ChosenSelect(),'coords': chosenforms.widgets.ChosenSelectMultiple(),'status': chosenforms.widgets.ChosenSelect()}

#to restrict coords for a core. Currently all coords display for a core. Code results in cups because of a cup in
#      # Let the Core save the SubTask
#            curr_subtask_form = SubTaskForm (request.POST, instance = curr_subtask)  line 336 in tasks/views.py  
#
#

#   The Curry issue has been fixed. However, when trying to edit a form, it does not change the form because it isn't valid 
#   for some reason. Line 469  if curr_subtask_form.is_valid (): returns FALSE. So the subtask just reloads itself without any changes.
#

    def __init__(self, editor=None, *args, **kwargs):
        if isinstance(editor,User):
            # The reason it is isinstance is because when i'm editing a subtask in particular, 
            # junk values are getting passed to editor in POST method.
            # To check, make it
        # if editor:
            # The code will fail but editor will be a random dictionary of variables.
            super(SubTaskForm, self).__init__(*args, **kwargs)
            print "THIS IS", editor
            self.fields['coords'].queryset = User.objects.filter(userprofile__department=editor.get_profile().department)
            self.fields['coords'].label_from_instance = lambda obj: "%s - %s" % (obj.get_profile ().name, obj.get_profile ().nickname)
            self.fields['coords'].help_text = ''
        else:
            super(SubTaskForm, self).__init__(editor,*args, **kwargs)   

        
#hack if these fields need to be formatted        
#    def __init__(self, *args, **kwargs):
#        super(SubTaskForm, self).__init__(*args, **kwargs)
#        self.fields['subject'].widget.attrs['rows'] = '500'
#        self.fields['subject'].widget.attrs['cols'] = '500'
        
