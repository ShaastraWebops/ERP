from django.db import models

# Create your models here.

class Budget(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.FloatField()
    department = models.ForeignKey(Department)
    comment = models.TextField(blank=True)
    event_core_status = models.BooleanField(default=False)
    finance_core_status = models.BooleanField(default=False)
    
class Item(models.Model):
    budget = models.ForeignKey(Budget)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    original_amount = models.FloatField()
    request_amount = models.FloatField()
    balance_amount = models.FloatField()   
    request_status = models.BooleanField(default=False)    
