from django.db import models

# Create your models here.




class Feedback(models.Model):
    email = models.CharField(max_length=255,null=True,blank=True) 
    username = models.CharField(max_length=255,null=True,blank=True) 
    message = models.TextField(null=True,blank=True)
    
    def __unicode__(self):
        return " Name = %s  email = %s" %(self.username,self.email)
    
