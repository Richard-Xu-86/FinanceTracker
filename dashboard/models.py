from django.db import models
from django.contrib.auth.models import User

class Graphprefer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE) #each user has one and only one Graphprefer object. 
    graph = models.CharField(max_length=255, blank=True, null=True) #Stores a text value (e.g., 'bar', 'pie', 'line') for the graph type.
    month = models.CharField(max_length=255, blank=True, null=True) #Stores the preferred month or time range the user wants to visualize.
    

    def __str__(self):
        return str(self.user)+"'s"+'preferences'

