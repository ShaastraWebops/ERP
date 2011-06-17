from django.db import models
from django.contrib.auth.models import User
from erp.department.models import *

# Create your models here.
class Coord_details(models.Model):
    coord_name=models.CharField(max_length=30)
    coord_email=models.CharField(max_length=50)    	

class Core(models.Model):
    user=models.ForeignKey(User,unique="True")
    department= models.ForeignKey(Department,related_name="dept_core_belong")
