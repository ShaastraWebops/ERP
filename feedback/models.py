# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from erp.department.models import Department
from erp.users.models import userprofile
from erp.misc.helper import is_core, is_coord, get_page_owner

STAT_CHOICES= (
    ('Core','Core'),
    ('Coord','Coordinator'),
    ('Vol','Volunteer'),
    ('All','All'),
)

class Question(models.Model):
    question = models.CharField(max_length=200)
    departments = models.ManyToManyField(Department)
    answered_by = models.CharField(max_length=5,choices=STAT_CHOICES,default = 'All')
    def __str__(self):
        return self.question
        
class Answer(models.Model):
    question = models.ForeignKey(Question)
    owner = models.ForeignKey(userprofile, related_name='answer_owner')
    creator = models.ForeignKey(userprofile, related_name='answer_creator')
    rating = models.IntegerField(blank=True,null=True)
    answered = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.rating      
        
class Answeravg(models.Model):
    question = models.ForeignKey(Question)
    owner = models.ForeignKey(userprofile)
    num = models.DecimalField(max_digits=6, decimal_places=2)
    avg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.avg
