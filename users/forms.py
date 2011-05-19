from django.db import models
from django.forms import ModelForm
from models import *

class UserProfileForm (ModelForm):
    class Meta:
        model = userprofile
