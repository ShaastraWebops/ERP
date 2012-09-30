from django.db import models
from django.contrib.auth.models import User

DEP_CHOICES = (
	("Events", "Events"),
	("QMS", "Quality Management"),
	("Finance", "Finance"),
	("Sponsorship", "Sponsorship and PR"),
	("Evolve", "Evolve"),
	("Facilities", "Facilities"),
	("MobOps", "Mobile Operations"),	
	("WebOps", "Website Operations"),
	("Hospitality", "Hospitality"),
	("Publicity", "Publicity"),
	("Design", "Design"),
)

# Create your models here.
#This is the initial department model
class Department(models.Model):
    Dept_Name= models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
    is_event=models.BooleanField(default=True)
    def __str__(self):
        return self.Dept_Name
        
    

