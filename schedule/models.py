from django.db import models

# Create your models here.

class Task(models.Model):

    task_subject     = models.CharField(max_length=100 , null=True , blank=True)
    task_description = models.TextField(null=True , blank=True)
    task_creator     = models.ForeignKey(User , related_name = "tasks_assigned")
    task_assigned_to = models.ManyToManyField(User, related_name = "tasks")
    #Task can be assigned to multiple people, say all webops coords etc. Think about how we can implement this by grouping coords etc
    task_deadline    = models.DateTimeField(null=True , blank=True)
    #Note that there must be a thread associated with each task 
