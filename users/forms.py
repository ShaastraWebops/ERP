from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
import re
alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")

#author :vivek kumar bagaria
#i changed it cause it was not working in the templates
class AddUserForm (forms.Form):
    username=forms.CharField(max_length=30,help_text='Enter a username. eg, siddharth_s')
    first_name=forms.CharField(max_length=30,help_text='Enter your first name. eg, Siddharth')
    last_name=forms.CharField(max_length=30,help_text='Enter your last name. eg, Swaminathan')
    email=forms.EmailField(help_text='Enter your e-mail address. eg, someone@gmail.com')
    password=forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput,help_text='Enter a password that you can remember')
    password_again=forms.CharField(max_length=30, widget=forms.PasswordInput,help_text='Enter the same password that you entered above')
    mobile_number=forms.CharField(max_length=15,help_text='Enter your mobile number. eg, 9884098840')
    department=forms.CharField(max_length=15)    
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_age(self):
	if (self.cleaned_data['age']>80 or self.cleaned_data['age']<12):
	    raise forms.ValidationError(u'Please enter an acceptable age (12 to 80)')
	else:
	    return self.cleaned_data['age']
	    
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	else:
	  return self.cleaned_data['mobile_number']
	  
    def clean_first_name(self):
	if not self.cleaned_data['first_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['first_name']
	  
    def clean_last_name(self):
	if not self.cleaned_data['last_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['last_name']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]
	    
    

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()   
