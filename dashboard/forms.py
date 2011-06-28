from django.db import models
from django.forms import ModelForm
from models import *
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
    short_description=forms.CharField(max_length=100)

    class Admin:
        pass

# class shout_box_form(forms.Form):
#     comments=forms.CharField(max_length=200)

""""

class change_pic(forms.Form):
    file  = forms.FileField()


"""
