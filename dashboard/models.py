from django.db import models
from django.contrib.auth.models import User
from erp.department.models import *
# Create your models here.
class teamdetails(models.Model):
    name=models.ForeignKey(User,unique=True)
    department=models.ForeignKey(Department )
    mobile_number=models.CharField(max_length=15)
    email_id=models.EmailField()
