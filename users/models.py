from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)
#List of Department Choices
<<<<<<< HEAD
#DEP_CHOICES    = (
#	("Events", "Events"),
#	("QMS", "Quality Management"),
#	("Finance", "Finance"),
#	("Sponsorship", "Sponsorship"),
#	("Evolve", "Evolve"),
#	("Facilities", "Facilities"),
#	("Webops", "Web Operations"),
#	("Hospitality", "Hospitality"),
#	("Publicity", "Publicity"),
#	("Design", "Design"),
#)

=======
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
	("Aerobotics","Aerobotics"),
	#We have to fill up with list of events
	("Webops","Web Operations")
)
>>>>>>> f701031dcda3cf86da9c115ecb3a0e3e462ad2d4

#This is the initial users model
#Author-Krishna Shrinivas

class userprofile(models.Model):
    user= models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')
    age = models.IntegerField(default=18,)
    department_belong = models.ManyToManyField(Department,related_name="dept_belong")
   
   #department_monitor=models.CharField(max_length=50,choices=DEP_CHOICES,default='Events') I feel this is unneccessary now.
    
    mobile_number = models.CharField(max_length=15)
    college_roll = models.CharField(max_length=40,default='Enter College Id/Roll No.')
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    
#We are changing to groups right? so, i removed the flags.
 
    #i Havent written the methods as yet, do we use them as methods in a class or in views?
    def __str__(self):

        return self.user.username

    class Admin:
        pass

#author : vivek kumar bagaria
<<<<<<< HEAD
class Materials(model.Model):
	user		=models.ForeignKey(User, unique=True)#name of the  person who asked or gave
	item		=models.CharField(max_length=50)# the material which has been asked for
	item_no		=models.IntergerField(default=1)#no. of items borrowed
	borrowed_time   =models.DateTimeField(null=True ,blank=True)#time of borrow
	return_time 	=models.DateTimeField(null=True ,blank=True)#time of return
	item_got	=models.BooleanField(default=False)#if the person got/given the item this will be true
	item_returned	=models.BooleanField(default=False)#if the person returns/takes the item this will be true
	user_2		=models.ForeignKey(User , unique=True)#name of the person/hostel/deptartment borrowed/lent from
    
	def __str__(self):

=======
class Materials(models.Model):
    user	  = models.ForeignKey(User, unique=True)#name of the  person who asked or gave
#					   ^^^^^^^^^^^	-----shouldnt that be a foreign key to User?	
    item	  = models.CharField(max_length=50)# the material which has been asked for
    item_no	  = models.IntegerField(default=1)#no. of items borrowed
    borrowed_time = models.DateTimeField(null=True ,blank=True)#time of borrow
    return_time   = models.DateTimeField(null=True ,blank=True)#time of return
    item_got      = models.BooleanField(default=False)#if the person got/given the item this will be true
    item_returned = models.BooleanField(default=False)#if the person returns/takes the item this will be true
    user_2        = models.CharField(max_length=40)#name of the person/hostel/deptartment borrowed/lent from
    #Isn't this also a foreign key to User?  
    def __str__(self):
>>>>>>> f701031dcda3cf86da9c115ecb3a0e3e462ad2d4
        return self.item

    class Admin:
        pass


