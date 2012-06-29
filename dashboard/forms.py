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
    class Meta:
        widgets = {'title': forms.Textarea(attrs={'cols': 80, 'rows': 20}),}


class shout_box_form(ModelForm):
    class Meta:
        model=shout_box
        exclude = ('user','nickname','timestamp')
""""

class change_pic(forms.Form):
    file  = forms.FileField()


"""
