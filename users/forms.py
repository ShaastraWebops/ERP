from django.db import models
from django.forms import ModelForm
from models import *
from django import forms

#author :vivek kumar bagaria
#i changed it cause it was not working in the templates
class UserProfileForm(forms.Form):
    user_name=forms.CharField()
    first_name=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput , label="maama passowrd")
    password_again=forms.CharField(widget=forms.PasswordInput , label="maama passowrd again")
    email=forms.EmailField(label="your email ")
    last_name=forms.CharField()
    department=forms.CharField()
    mobile_number=forms.IntegerField()
    department_monitor=forms.CharField()
    
	

class UserLoginForm(forms.Form):
    username=forms.CharField(help_text='Your username as registered with the ERP')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()   
