from django.db import models
from django.forms import ModelForm
from feedback.models import *
from django import forms

class QuestionForm (ModelForm):
    class Meta:
        model = Question
