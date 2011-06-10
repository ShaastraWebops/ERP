from django.db import models
from django.forms import ModelForm
from models import *
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.ImageField()
    short_description=forms.CharField(max_length=100)
