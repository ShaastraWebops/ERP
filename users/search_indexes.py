"""import datetime
from haystack.indexes import *
from haystack import site
from users.models import *

   

class userprofileindex(indexes.SearchIndex):
    text        =indexes.CharField(document=True,use_template=True)
    nickname    =indexes.CharField(model_attr='nickname')
    name        =indexes.CharField(model_attr='name')
    hostel 	=indexes.CharField(model_attr='hostel')
    summer_stay =indexes.CharField(model_attr='room_no')
    
    #email_id    =indexes.EmailField(model_attr='email_id')

    def index_queryset(self):

        return userprofile.objects.all()#pub_date=datetime.datetime.now())

site.register(userprofile,userprofileindex)

"""