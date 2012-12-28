from django.db import models
from erp.department.models import Department
from django.contrib.auth.models import User

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class Prize(models.Model):
    """
    The winner's details and cheque nos
    """
    Name=models.CharField(max_length=30)
    Position=models.CharField(max_length=10)
    contact=models.CharField(max_length=15)
    event=models.ForeignKey(Department)
    details=models.CharField(max_length=250)
    cheque=models.CharField(max_length=15)
    # User who is uploading the entry
    user=models.ForeignKey(User)

class Participant(models.Model):
    """
    The participant's data.
    """
    barcode = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              default='F')
    age = models.IntegerField(default=18)
    branch = models.CharField(max_length=50, blank=True, null=True,
                              help_text='Your branch of study')
    mobile_number = models.CharField(max_length=15, null=True,
            help_text='Please enter your current mobile number')
    college = models.CharField(max_length=100)
    college_roll = models.CharField(max_length=40, null=True)
    events = models.ManyToManyField(Department,
            related_name='participants', null=True)

"""
I suggest we shift to this Prize model:

class Prize(models.Model):
    \"""
    The winner's details and cheque nos
    \"""
    participant = models.ForeignKey(Participant)
    position = models.CharField(max_length=10)
    event = models.ForeignKey(Department)
    details = models.CharField(max_length=250)
    cheque = models.CharField(max_length=15)
    # User who is uploading the entry
    user = models.ForeignKey(User)
"""
