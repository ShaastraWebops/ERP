from django.db import models
from django.contrib.auth.models import User

DEP_CHOICES = (
	("Events", "Events"),
	("QMS", "Quality Management"),
	("Finance", "Finance"),
	("Sponsorship", "Sponsorship"),
	("Evolve", "Evolve"),
	("Facilities", "Facilities"),
	("Webops", "Web Operations"),
	("Hospitality", "Hospitality"),
	("Publicity", "Publicity"),
	("Design", "Design"),
)

# Create your models here.
#This is the initial department model
class Department(models.Model):
    Dept_Name= models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
    def __str__(self):
        return self.Dept_Name
        
    

