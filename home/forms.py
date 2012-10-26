from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from django.contrib.auth.forms import PasswordResetForm

from django.contrib.auth.hashers import UNUSABLE_PASSWORD, is_password_usable, get_hasher

class UserLoginForm(forms.Form):
    username=forms.CharField(help_text='Your username as registered with the ERP')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password. If you do not remember this, please use the link below')
    
class forgot_password_form(ModelForm):
	
	class Meta:
		model=forgot_password
		exclude=('date',)
		
class ModifiedPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        query = User.objects.filter(email__iexact=email,
                                               is_active=True)
        user = User.objects.filter(username=sortlist([x.username for x in query])[-1])
        self.users_cache = user
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email
        
def bylength(word1,word2):
    return len(word2)-len(word1)

def sortlist(a):
    a.sort(cmp=bylength)
    return a	

