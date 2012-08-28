from django.db import models

class Tabs(model.Model):
    title   =models.Charfield(max_length=100)
    URL     =models.Charfield(null=True)
    # each page will have different tabs which will be hyperlinked
    #like in the erp 2 document
    
    


