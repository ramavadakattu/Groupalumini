from django.db import models

# Create your models here.


class Country(models.Model) :    
    name = models.CharField(max_length=100)    
    
    
    def __unicode__(self):
        return "%s"%(self.name,)
        



class State(models.Model):    
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country)    
    
    def __unicode__(self):
        return "%s"%(self.name,)
         