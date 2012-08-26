import datetime
from haystack.indexes import *
from haystack import site
from erp.users.models import *

   

class userprofileindex(RealTimeSearchIndex):
    text        =CharField(document=True,use_template=True)
    nickname    =CharField(model_attr='nickname')
    name        =CharField(model_attr='name')
    hostel 	=CharField(model_attr='hostel')
    summer_stay =CharField(model_attr='room_no')
    
    #email_id    =CharField(model_attr='email_id')

    def index_queryset(self):

        return userprofile.objects.all()#pub_date=datetime.datetime.now())

site.register(userprofile,userprofileindex)


