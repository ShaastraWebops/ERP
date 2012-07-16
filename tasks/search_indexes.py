import datetime
from haystack.indexes import *
from haystack import site
from erp.tasks.models import *


class taskindex(RealTimeSearchIndex):
    text        =CharField(document=True,use_template=True)
    subject     =CharField(model_attr='subject',null=True)
    description =CharField(model_attr='description',null=True)
    status      =CharField(model_attr='status',null=True)


site.register(Task,taskindex)

class SubTaskIndex(RealTimeSearchIndex):
    text        =CharField(document=True,use_template=True)
    subject     =CharField(model_attr='subject', null=True)
    description =CharField(model_attr='description', null=True)
    status      =CharField(model_attr='status', null=True)
    department  =CharField(model_attr='department')

site.register(SubTask, SubTaskIndex)
