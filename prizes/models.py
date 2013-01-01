from django.db import models
from erp.department.models import Department
from django.contrib.auth.models import User

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

class Participant(models.Model):
    """
    The participant's data.
    """
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
    shaastra_id = models.CharField(max_length=30, blank=True)
    events = models.ManyToManyField(Department,
            related_name='participants', null=True)
    
    def __str__(self):
        return self.shaastra_id

class BarcodeMap(models.Model):
    """
    Maps barcode to participant
    """
    barcode = models.CharField(max_length=128,blank=True)
    shaastra_id = models.ForeignKey(Participant, blank=True, null=True)  
    
    def __str__(self):
        return self.barcode
        
class Prize(models.Model):
    """
    The winner's details and cheque nos
    """
    participant = models.ForeignKey(Participant,blank=True, null=True)
    position = models.CharField(max_length=10,blank=True)
    event = models.ForeignKey(Department)
    details = models.CharField(max_length=250,blank=True)
    cheque = models.CharField(max_length=15,blank=True)
    # User who is uploading the entry
    user = models.ForeignKey(User)  
    
    def __str__(self):
        return self.participant.shaastra_id

class College(models.Model):

    name = models.CharField(max_length=255,
                            help_text='The name of your college. Please refrain from using short forms.'
                            )
    city = models.CharField(max_length=30,
                            help_text='The name of the city where your college is located. Please refrain from using short forms.'
                            )
    state = models.CharField(max_length=40,help_text='The state where your college is located. Select from the drop down list'
                             )

    def __unicode__(self):
        return '%s, %s, %s' % (self.name, self.city, self.state)

    class Admin:
        pass

    class Meta:
        db_table='users_college'

class ParticipantUser(models.Model):
    user=models.ForeignKey(User)
    gender = models.CharField(max_length=1,
                              default='F')
    age = models.IntegerField(default=18)
    branch = models.CharField(max_length=50, blank=True, null=True,
                              help_text='Your branch of study')
    mobile_number = models.CharField(max_length=15, null=True,
            help_text='Please enter your current mobile number')
    college = models.ForeignKey(College, null=True, blank=True)
    college_roll = models.CharField(max_length=40, null=True)

    shaastra_id = models.CharField(max_length = 20, unique = True, null=True)

    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)
    want_accomodation = models.BooleanField(default=False, help_text = "This doesn't guarantee accommodation during Shaastra.")
    is_core = models.BooleanField(default=False)
    is_hospi = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=20)
    access_token = models.CharField(max_length=250)

    class Admin:
        pass
        
    class Meta:
        db_table='users_userprofile'

