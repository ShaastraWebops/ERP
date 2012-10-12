from django.db import models
from django.contrib.auth.models import User

DEP_CHOICES = (
("QMS", "Quality Management"),
("Finance", "Finance"),
("MobOps", "MobOps"),
("WebOps", "WebOps"),
("Hospitality", "Hospitality"),
("Publicity", "Publicity"),
("Graphic Design", "Graphic Design"),
("Photography", "Photography"),
("Ambience", "Ambience"),
("Creative Design", "Creative Design"),
("Videography", "Videography"),
("Air Show", "Air Show"),
("Wright Design", "Wright Design"),
("Paper Plane", "Paper Plane"),
("Aerobotics", "Aerobotics"),
("Hackfest", "Hackfest"),
("OPC", "OPC"),
("Reverse Coding", "Reverse Coding"),
("Triathlon", "Triathlon"),
("Robowars", "Robowars"),
("Contraptions", "Contraptions"),
("Fire n Ice", "Fire n Ice"),
("Robotics", "Robotics"),
("Junkyard Wars", "Junkyard Wars"),
("Ultimate Engineer", "Ultimate Engineer"),
("Project X", "Project X"),
("Shaastra Cube Open", "Shaastra Cube Open"),
("Puzzle Champ", "Puzzle Champ"),
("Math Modelling", "Math Modelling"),
("Shaastra Main Quiz", "Shaastra Main Quiz"),
("Online Events", "Online Events"),
("Desmod", "Desmod"),
("SCDC", "SCDC"),
("Robo-Oceana", "Robo-Oceana"),
("Gamedrome", "Gamedrome"),
("IDP", "IDP"),
("Shaastra Junior", "Shaastra Junior"),
("Sustainable Cityscape", "Sustainable Cityscape"),
("Case Study", "Case Study"),
("Fox Hunt", "Fox Hunt"),
("Magic Materials", "Magic Materials"),
("Computer Literacy For All", "Computer Literacy For All"),
("Face Off", "Face Off"),
("Sketch It", "Sketch It"),
("Pilot Training", "Pilot Training"),
("Hovercraft", "Hovercraft"),
("Lectures and VCs", "Lectures and VCs"),
("Shaastra Nights", "Shaastra Nights"),
("Symposium", "Symposium"),
("Exhibitions", "Exhibitions"),
("IITM Ideas Challenge", "IITM Ideas Challenge"),
("GA PA Materials", "GA/PA Materials"),
("Production", "Production"),
("Equipment", "Equipment"),
("Catering", "Catering"),
("VIP Care", "VIP Care"),
("Prize and Prize Money", "Prize and Prize Money"),
("Sales and Distribution", "Sales and Distribution"),
("Analytics", "Analytics"),
("Spons Creative", "Spons Creative"),
("Spons Publicity", "Spons Publicity"),
("Sponsorship and PR", "Sponsorship and PR"),
("Vishesh", "Vishesh"),
("Newsletter and PR", "Newsletter and PR"),
)

# This is the initial department model
class Department(models.Model):
    Dept_Name= models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
    # In case of multiple owners
    owner = models.ManyToManyField(User, blank=True, null=True)
    def __str__(self):
        return self.Dept_Name
        
    

