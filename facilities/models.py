from django.db import models
from erp.department.models import Department
from erp.users.models import userprofile
from django.db.models import Q
import datetime
# Create your models here.
DATE_CHOICES=( ('5th January, 2012','5th January, 2012'),('6th January, 2012','6th January, 2012'),
               ('7th January, 2012','7th January, 2012'),('8th January, 2012','8th January, 2012') )
HOUR_CHOICES=( (00,00),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
               (8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),
               (16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23) )
MINUTE_CHOICES=( (00,00),(15,15),(30,30),(45,45) )
SUPPLIER_CHOICES=( ('GA,GA'),("Materials","Materials"),("PA","PA"),("Equipment","Equipment"),("Other","Other") )
VENUE_CHOICES=( ("SAC","SAC") , ("CRC","CRC"),("ICSR","ICSR"),("CLT","CLT") )


class EventRound(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField(max_length = 25,blank=True)
    department = models.ForeignKey(Department)
    venue = models.CharField(max_length=20,blank=True,null=True,choices=VENUE_CHOICES)
    start_date = models.CharField(max_length=20,blank=True,null=True,choices=DATE_CHOICES)
    start_hour = models.IntegerField(blank=True,null=True,choices=HOUR_CHOICES)
    start_minute = models.IntegerField(blank=True,null=True,choices=MINUTE_CHOICES)
    end_date = models.CharField(max_length=20,blank=True,null=True,choices=DATE_CHOICES)
    end_hour = models.IntegerField(blank=True,null=True,choices=HOUR_CHOICES)
    end_minute = models.IntegerField(blank=True,null=True,choices=MINUTE_CHOICES)
    

class ItemList(models.Model):
    name = models.CharField(max_length = 50,blank=True)
    department = models.ForeignKey(Department,null=True)

    def __str__(self):
        return self.name

class FacilitiesObject(models.Model):
    #creator = models.ForeignKey(userprofile)
    department = models.ForeignKey(Department,null = True,limit_choices_to = Q(id__range=(57,62)))
    event_round = models.ForeignKey(EventRound)
    name = models.ForeignKey(ItemList)
    quantity=models.IntegerField(blank=True,null=True,default=0)
    #approved_quantity = models.IntegerField(default=0)
    #description = models.TextField(blank=True)
    #comment = models.TextField(blank=True)
    #request_status = models.IntegerField(default=0)  
    #request_date = models.DateField(blank=True)
    #approved_by = models.CharField(max_length=50,blank=True)
    rec_fac = models.DecimalField(max_digits=7,decimal_places=6,default=1)

