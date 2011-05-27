from django.db import models
from django.contrib.auth.models import User
from erp.department.models import Department

# Create your models here.
#The choices may be cup level but if any thing better pls do change.
STAT_CHOICES= (
	('O','Open'),
	('C','Completed'),
	('L','Overdue'),
	('N','Almost'),
)

DEFAULT_STATUS = 'O'
    
class AbstractBaseTask(models.Model):
    """ Abstract Base Class for Task, SubTask.

    TODO:
    * File upload
    * Draft saving
    * QMS Manager for the Task
    """
    subject       = models.CharField(max_length=100 , null=True)
    description   = models.TextField(null=True , blank=True)
    creator       = models.ForeignKey(User, related_name = '%(app_label)s_%(class)s_creator')
    creation_date = models.DateTimeField (auto_now = True, editable = False)
    deadline      = models.DateField(null=True , blank=True)
    status        = models.TextField(max_length=50,choices=STAT_CHOICES,default = DEFAULT_STATUS)	
    class Meta:
        abstract = True
        
class Task(AbstractBaseTask):

    """ Task Model

    Note : The department where the Task originated is understood from
    the Creator's department. As of now, only Cores can create Tasks.

    A Task mainly consists of SubTasks which are created and assigned by the respective Cores of each department.
    """

    def __str__(self):
        return self.subject

    class Admin:
        pass

class SubTask(AbstractBaseTask):
    """ SubTask Model

    As of now, SubTasks can be created mainly in two places :

    * When a Core breaks Tasks down into SubTasks and assigns some of
      them to Coords in his own department and/or delegates a SubTask
      to another Department (whose core has to then assign that
      SubTask to that department's coords, possibly creating more
      SubTasks as required)

    * When a Coord creates goals with deadlines for himself (these are
      called SubTasks but will actually be shown in his Timeline and
      handled differently from SubTasks that have been assigned to him
      by Cores)
    """
    coords = models.ManyToManyField (User, blank = True)
    department = models.ForeignKey (Department)
    task = models.ForeignKey (Task)

    def __str__(self):
        return self.subject

    class Admin:
        pass

class AbstractComment (models.Model):
    """ Abstract Base Class to store a comment.

    Timestamp helps to order comments. It is generated automatically.
    Author can be used to select particular comments based on the author.
    """
    author = models.ForeignKey (User, related_name = '%(app_label)s_%(class)s_author')
    comment_string = models.TextField ()
    time_stamp = models.DateTimeField (auto_now = True, editable = False)

    class Meta:
        abstract = True

class TaskComment(AbstractComment):
    """ Comment written for a Task.
    """
    task = models.ForeignKey (Task)

    def __str__(self):
        return '%s %s' %(self.task.subject, self.id)
    class Admin:
        pass
        
class SubTaskComment(AbstractComment):
    """ Comment written for a SubTask
    """
    subtask = models.ForeignKey (SubTask)

    def __str__(self):
        return '%s %s' %(self.task.subject, self.id)
    class Admin:
        pass
        
class Label(models.Model):
    labelname = models.ForeignKey(Task, related_name="task_label")
