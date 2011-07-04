from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
import re

alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]

class AddUserForm (forms.Form):
    username = forms.CharField(max_length = 30,
                               help_text = 'your roll no number is your username')
    email = forms.EmailField(help_text = 'Enter your e-mail address. eg, someone@gmail.com',
                             required = False)
    password = forms.CharField(min_length = 6,
                               max_length = 30,
                               widget = forms.PasswordInput,
                               help_text = 'Enter a password you can remember')
    password_again = forms.CharField(max_length = 30,
                                     widget = forms.PasswordInput,
                                     help_text = 'Re-enter above password')

    def clean_username(self):
	if (len(self.cleaned_data['username']) != 8):
	    raise forms.ValidationError('please enter a valid roll number')
	else:
	    rollno = self.cleaned_data['username']
	    first = rollno[0:2]
	    second = rollno[2:4]
	    third = rollno[4:5]
	    fourth = rollno[5:8]
	    if not re.match("^[A-Za-z]*$",first):
	        raise forms.ValidationError('please enter a valid roll number')
	    if not re.match("^[A-Za-z]*$",third):
	        raise forms.ValidationError('please enter a valid roll number')
	    if not re.match("^[0-9]*$",second):
	        raise forms.ValidationError('please enter a valid roll number')
	    if not re.match("^[0-9]*$",fourth):
	        raise forms.ValidationError('please enter a valid roll number')
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username = self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_email(self):
        given_email = self.cleaned_data['email']
        if given_email == '':
            return given_email
        elif User.objects.filter(email = given_email):
            pass
        else:
            return  given_email
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
	    
class userprofileForm (ModelForm):
    class Meta:
	model = userprofile
	exclude = ('user',)

    def clean_chennai_number(self):
        number1 = self.cleaned_data['chennai_number']
        print "cleaning"
        if number1 == '':
            return number1
        elif ((len(number1)<9) or (len(number1)>12)):
            print "true"
            raise forms.ValidationError ("Enter a valid number")
        else :
            return self.data['chennai_number']
    def clean_name (self):
        """
        During Testing phase, name is required.
        """
        given_name = self.cleaned_data['name']
        if given_name == '':
            raise forms.ValidationError ('Please enter your name.')
        return given_name
        
class invite_coord(forms.Form):
    name = forms.CharField(max_length = 50)
    email_id = forms.CharField(help_text = "coords email")

class InviteForm (ModelForm):
    class Meta:
        model = invitation
        exclude = ('core' , 'time')


class change_pic(forms.Form):
    file = forms.FileField()

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length = 50)
    file = forms.FileField()
    short_description = forms.CharField(max_length = 100)


