from django.db import models
from erp.department.models import Department
from erp.users.models import userprofile
from django.db.models import Q
import datetime
# Create your models here.

class FacilitiesObject(models.Model):
    creator = models.ForeignKey(userprofile)
    department = models.ForeignKey(Department,limit_choices_to = Q(id__range=(57,62)))
    name = models.CharField(max_length=50)
    quantity=models.IntegerField(blank=True,null=True)
    approved_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    request_status = models.IntegerField(default=0)  
    request_date = models.DateField(blank=True)
    approved_by = models.CharField(max_length=50,blank=True)
