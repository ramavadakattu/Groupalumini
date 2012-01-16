from django.db import models

# Create your models here.
class Industry(models.Model):
    name = models.CharField(max_length=200,unique=True)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Industry = %s"%(self.name,)
    
    
    
class Market(models.Model):
    name = models.CharField(max_length=120,unique=True)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    industries = models.ManyToManyField(Industry)
    
        
    def __unicode__(self):
        ids = []
        for i in self.industries.all() :
            ids.append(i.name)
            
        return "Market ==> %s Industries ==> %s "%(self.name,",".join(ids))