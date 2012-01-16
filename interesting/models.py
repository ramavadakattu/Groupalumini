from django.db import models
from tagging.models import Tag
from django.contrib.auth.models import User

# Create your models here.


class UserTagWeight(models.Model):
    ''' weightage of single tag for a given user'''
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    weight = models.IntegerField(default=0)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)    
    
    #For profile weightage is 10 , for creation weightage is 5
    #For seeing weightage is 1
    
    def __unicode__(self):
        return "%s %s weight = %s"%(self.user.get_profile().fullname,self.tag.name,str(self.weight))
    
    
    
    
    
    
    

