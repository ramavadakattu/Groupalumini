from django.db import models
from institution.models import Institution
from django.contrib.auth.models import  User
from  django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.html import linebreaks , strip_tags

# Create your models here.
import logging
import logging.config

import tagging



mlogger = logging.getLogger(__name__)

''' Ask alumini  emulating  mini stackoverflow '''


        
class Comment(models.Model):
    text = models.TextField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)    
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')    
    
    
    def getNText(self):        
        ntext = strip_tags(self.text)
        return ntext.replace("\n","<br/>")
    
    
    def __unicode__(self):
        return "comment = %s" %(self.text[:50])



class Question(models.Model):
    subject = models.CharField(max_length=1024)
    description = models.TextField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    institute = models.ForeignKey(Institution)
    user = models.ForeignKey(User)
    comments = generic.GenericRelation(Comment)
    
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('displayquestionurl',(),{'questionno': self.id})
    
    
    def __unicode__(self):
        return "question subject %s in institute %s" %(self.subject,self.institute.name)     

         
try :
    tagging.register(Question)
except tagging.AlreadyRegistered :
    pass  
            
        
        
class Answer(models.Model):
    text = models.TextField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)    
    user = models.ForeignKey(User)
    question  = models.ForeignKey(Question)
    comments = generic.GenericRelation(Comment)
  
    
    def __unicode__(self):
        return "answer = %s" %(self.text[:50])
        
        
