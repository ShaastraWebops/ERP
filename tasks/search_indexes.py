import datetime
from haystack.indexes import *
from haystack import site
from erp.tasks.models import *


class taskindex(SearchIndex):
    text        =CharField(document=True,use_template=True)
    subject     =CharField(model_attr='subject')
    description =CharField(model_attr='description')
    status      =CharField(model_attr='status')


site.register(Task,taskindex)