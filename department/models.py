from django.db import models


DEP_CHOICES    = (
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
class Department(models.Model)

	Dept_Name= models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
	Dept_Cores=models.ManyToManyField(User, related_name = "department")
#This is done assuming that cores are just users with relevant permissions

