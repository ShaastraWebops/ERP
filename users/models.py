from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from erp.department.models import *
from django.conf import settings
# Create your models here.

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)

HOSTEL_CHOICES  =(
        ("Ganga", "Ganga"),
        ("Mandak", "Mandak"),
        ("Jamuna", "Jamuna"),
        ("Alak", "Alak"),
        ("Saraswati", "Saraswati"),
        ("Narmada", "Narmada"),
        ("Godav", "Godav"),
        ("Pampa", "Pampa"),
        ("Tambi", "Tambi"),
        ("Sindhu", "Sindhu"),
        ("Mahanadi", "Mahanadi"),
        ("Sharavati", "Sharavati"),
        ("Krishna", "Krishna"),
        ("Cauvery", "Cauvery"),
        ("Tapti", "Tapti"),
        ("Bhramhaputra", "Bhramhaputra"),
        ("Sarayu", "Sarayu"),
        )

class userprofile(models.Model):
    """
    User's profile which contains all personal data.
    """
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    department = models.ForeignKey(Department)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True)
    room_no = models.IntegerField(default=0, blank=True)

    class Meta:
        pass

    def __str__(self):
        return '%s %s' %(self.user.username, self.hostel)

    class Admin:
        pass

class Materials(models.Model):
    # name of the  person who asked or gave
    user = models.ForeignKey(User, unique=True, related_name="item_borrower")
    # the material which has been asked for
    item = models.CharField(max_length=50)
    # no. of items borrowed
    item_no = models.IntegerField(default=1)
    # time of borrow
    borrowed_time = models.DateTimeField(null=True ,blank=True)
    # time of return
    return_time = models.DateTimeField(null=True ,blank=True)
    # if the person got/given the item this will be true
    item_got = models.BooleanField(default=False)
    # if the person returns/takes the item this will be true
    item_returned = models.BooleanField(default=False)
    # name of the person/hostel/deptartment borrowed/lent from
    user_2 = models.ForeignKey(User , unique=True, related_name="item_lender")

    def __str__(self):
        return self.item

    class Admin:
        pass

class invitation(models.Model):
    core = models.ForeignKey(User , related_name="the core who has invited the user")
    invitee = models.CharField(max_length=50)#name of the coord
    roll_no = models.CharField(max_length=8)
    email_id = models.EmailField()
    time = models.DateField()

    class Admin:
	pass

class userphoto(models.Model):
    name=models.ForeignKey(User)
    photo_path=models.FileField(upload_to=settings.MEDIA_ROOT)

    def __str__(self):
	return str(self.photo_path)
    class Admin:
	pass

