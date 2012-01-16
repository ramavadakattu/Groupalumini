from django.db import models
from django.contrib.auth.models import User
from django.utils.html import linebreaks , strip_tags ,escape , urlize
import settings

# Create your models here.
import logging
import logging.config



mlogger = logging.getLogger(__name__)


class ShortMessages(models.Model) :
    ''' helps to store all the short messages that is user has been contacted'''
    fromuser = models.ForeignKey(User,related_name='messagessent')
    touser = models.ForeignKey(User,related_name='messagesrecieved') 
    text = models.CharField(max_length=settings.SHORT_MSG_CHARS)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    
    def getNText(self,ajax=False):        
        ntext = self.text.strip()
        ntext = strip_tags(ntext)
        ntext = ntext.strip()
        
        ntext = escape(ntext)
        ntext = urlize(ntext)   
        return ntext.replace("\n","<br/>")
        
        
    def __unicode__(self):
        return "Message ==> %s" %(self.getNText(),)
    
      
    
    
    

