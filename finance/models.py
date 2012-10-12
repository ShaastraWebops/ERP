from django.db import models
from erp.department.models import Department
from erp.users.models import userprofile
# Create your models here.

class Budget(models.Model):
    name = models.CharField(max_length=1)
    total_amount = models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    department = models.ForeignKey(Department)
    comment = models.TextField(blank=True)
    event_core_status = models.BooleanField(default=False)
    finance_core_status = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
        
class Item(models.Model):
    budget = models.ForeignKey(Budget)
    department = models.ForeignKey(Department)
    name = models.CharField(max_length=50)
    quantity=models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    original_amount = models.FloatField()
    request_amount = models.FloatField(blank=True, null=True)
    balance_amount = models.FloatField(blank=True, null=True)   
    request_status = models.BooleanField(default=False)  
    
class OpenBudgetPortal(models.Model):
    opened = models.BooleanField(default=False)
    
class Permission(models.Model):
    coord = models.CharField(max_length=25)
    budget_sanction = models.BooleanField(default=False)
    
class Deadline(models.Model):
    budget_portal_deadline=models.DateTimeField()
    
               
