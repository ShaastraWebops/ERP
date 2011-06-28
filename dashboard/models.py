from django.db import models
from django.contrib.auth.models import User
from erp.department.models import *
from django.conf import settings
class teamdetails(models.Model):
    name = models.ForeignKey(User,unique = True)
    department = models.ForeignKey(Department )
    mobile_number = models.CharField(max_length = 15)
    email_id = models.EmailField()

    class Admin:
	pass


class upload_documents(models.Model):
    user = models.ForeignKey(User)
    file_name = models.CharField(max_length = 25)
    file_path = models.FileField(upload_to = settings.MEDIA_ROOT )
    url = models.URLField(verify_exists = True )
    topic = models.CharField(max_length = 100,blank = True)#short description
    date = models.DateField()


    def __str__(self):
        return (self.file_path)
    

    class Admin:
	pass

# class shout_box(models.Model):
#     user = models.ForeignKey(User)
#     nickname = models.CharField(max_length = 50)
#     comments = models.TextField()
#     time_stamp = models.DateTimeField(editable = False)

#     class Meta:
#         ordering = ['time_stamp']
