from django.db import models
from erp.department.models import Department
from django.contrib.auth.models import User

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
