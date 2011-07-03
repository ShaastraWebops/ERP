import datetime
from haystack.indexes import *
from haystack import site
from tasks.models import *


class taskindex(indexes.SearchIndex):
    text        =indexes.CharField(document=True,use_template=True)
    subject     =indexes.CharField(model_attr='subject')
    description =indexes.CharField(model_attr='description')
    status      =indexes.CharField(model_attr='status')


site.register(Task,taskindex)
