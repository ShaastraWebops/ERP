import datetime
from haystack import indexes
from haystack import site
from users.models import *
"""

class userprofile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    email_id = models.EmailField(blank=True)
    department = models.ForeignKey(Department)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES)
    room_no = models.IntegerField(default=0, blank=True)
    
    """

class userprofileindex(indexes.SearchIndex):
    text=indexes.CharField(document=True,use_template=True)
    nickname    =indexes.CharField(model_attr='nickname')
    name        =indexes.CharField(model_attr='name')
    hostel 	=indexes.CharField(model_attr='hostel')
    #email_id    =indexes.EmailField(model_attr='email_id')

    def index_queryset(self):

        return userprofile.objects.all()#pub_date=datetime.datetime.now())


site.register(userprofile,userprofileindex)

    
