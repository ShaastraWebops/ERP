from django.db import models
from django.forms import ModelForm
from models import *

# class CommentForm (ModelForm):
#     class Meta:
#         model = Comment

class TaskForm (ModelForm):
    class Meta:
        model = Task
