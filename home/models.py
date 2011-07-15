from django.db import models
from django.contrib.auth.models import User
from erp.department.models import *
from django.conf import settings


class forgot_password(models.Model):
	username=models.CharField(max_length=100)
	email_id=models.EmailField()
	date=models.DateTimeField()
	
