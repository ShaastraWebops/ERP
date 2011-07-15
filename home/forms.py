from django.db import models
from django.forms import ModelForm
from models import *
from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(help_text='Your username as registered with the ERP')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')
    
class forgot_password_form(ModelForm):
	
	class Meta:
		model=forgot_password
		exclude=('date',)
		
		

