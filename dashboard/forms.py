from django.db import models
from django.forms import ModelForm
from models import *
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50 ,  widget =forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    file  = forms.FileField()
    short_description=forms.CharField(max_length=100)

    class Admin:
        pass
    class Meta:
        widgets = {'title': forms.Textarea(attrs={'cols': 80, 'rows': 20}),}


class shout_box_form(forms.Form):
    comments=forms.CharField(max_length=200)

""""

class change_pic(forms.Form):
    file  = forms.FileField()


"""
