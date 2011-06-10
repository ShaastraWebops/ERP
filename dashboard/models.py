from django.db import models
from django.contrib.auth.models import User
from erp.department.models import *
from django.conf import settings
class teamdetails(models.Model):
    name=models.ForeignKey(User,unique=True)
    department=models.ForeignKey(Department )
    mobile_number=models.CharField(max_length=15)
    email_id=models.EmailField()


class upload_documents(models.Model):
    user=models.ForeignKey(User)
    file_name=models.CharField(max_length=25)
    file_path=models.FileField(upload_to=settings.MEDIA_ROOT)
    topic=models.CharField(max_length=100,blank=True)#short description
    date=models.DateField()


    def __str__(self):
        return (self.file_path)
    
    
