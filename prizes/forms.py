from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from erp.prizes.models import *
from django.contrib.auth.models import User
#from chosen import widgets as chosenwidgets

class TaskCommentForm (ModelForm):
	comment_string=forms.CharField(label='Comments',widget=forms.Textarea)
	class Meta:
		model=TaskComment
		exclude=('author','task')	
