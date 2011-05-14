from django.db import models
from django.contrib import admin

# Create your models here.

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)
#List of Department Choices
DEP_CHOICES    = (
	("Events", "Events"),
	("QMS", "Quality Management"),
	("Finance", "Finance"),
	("Sponsorship", "Sponsorship"),
	("Evolve", "Evolve"),
	("Facilities", "Facilities"),
	("Webops", "Web Operations"),
	("Hospitality", "Hospitality"),
	("Publicity", "Publicity"),
	("Design", "Design"),
)
SUB_DEP_CHOICES = (
	("Aerobotics","Aerobotics")
	#We have to fill up with list of events
	("Webops","Web Operations")
)

#This is the initial users model
#Author-Krishna Shrinivas

class userprofile(models.Model):
    user= models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    age = models.IntegerField(default=18,)
    department_belong = models.CharField(max_length=50,choices=DEP_CHOICES,default='Webops')
    #This is for QMS co-ords as they will monitor a different department,for others it is the same department
    department_monitor=models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
    mobile_number = models.CharField(max_length=15)
    college_roll = models.CharField(max_length=40,default='Enter College Id/Roll No.')
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    is_core=models.BooleanField(default=False,blank=True)
    is_coord=models.BooleanField(default=False,blank=True)
    #This is for the sub-department, eg.Chemical-X, SMQ etc within Events
    sub_department=models.CharField(max_length=50,choices=SUB_DEP_CHOICES,default='Webops')
  
    #i Havent written the methods as yet, do we use them as methods in a class or in views?
    def __str__(self):

        return self.user.username

    class Admin:
        pass
#There was a duplication, i removed it.
