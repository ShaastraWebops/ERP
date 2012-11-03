from django.db import models
from erp.department.models import Department
from erp.users.models import userprofile
from django.db.models import Q
import datetime
# Create your models here.

class EventRound(models.Model):
    number = models.IntegerField(default=0)
    department = models.ForeignKey(Department)

class ItemList(models.Model):
    name = models.CharField(max_length = 50,blank=True)
    department = models.ForeignKey(Department,null=True)

    def __str__(self):
        return self.name

class FacilitiesObject(models.Model):
    creator = models.ForeignKey(userprofile)
    department = models.ForeignKey(Department,limit_choices_to = Q(id__range=(57,62)))
    roundno = models.IntegerField(default=0)
    name = models.ForeignKey(ItemList)
    quantity=models.IntegerField(blank=True,null=True)
    approved_quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    request_status = models.IntegerField(default=0)  
    request_date = models.DateField(blank=True)
    approved_by = models.CharField(max_length=50,blank=True)


        
