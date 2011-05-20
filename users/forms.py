from django.db import models
from django.forms import ModelForm
from models import *

class UserProfileForm(ModelForm):
    class Meta:
        model = userprofile

class UserLoginForm(forms.Form):
    username=forms.CharField(help_text='Your username as registered with the ERP')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()   
