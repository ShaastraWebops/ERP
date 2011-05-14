from django.db import models

# Create your models here.

class Task(models.Model):

    subject        = models.CharField(max_length=100 , null=True , blank=True)
    description    = models.TextField(null=True , blank=True)
    creator        = models.ForeignKey(User , related_name = "tasks_assigned")
    assigned_to    = models.ManyToManyField(User, related_name = "tasks")
    #Task can be assigned to multiple people, say all webops coords etc. Think about how we can implement this by grouping coords etc
    deadline       = models.DateTimeField(null=True , blank=True)
    # Why is this a TextField ? Shouldn't it have a dropdown list of various status messages like ASSIGNED, COMPLETED, SUSPENDED, etc.?
    status         = models.TextField(null=True , blank =True)
    flag_completed = models.BooleanField(default=False)
    #False - not completed, True - completed
    #Note that there must be a thread associated with each task 

class Comment (models.Model):
    """Model to store a comment.

    Timestamp helps to order comments
    Author can be used to select particular comments based on the author.
    """

    author = models.ForeignKey (User)
    time_stamp = models.DateTimeField (auto_now = True)
    comment_string = models.TextField ()
