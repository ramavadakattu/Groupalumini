from django.db import models
from institution.models import UserProfile
import settings

# Create your models here.

class Connection(models.Model):
      initiator = models.ForeignKey(UserProfile,related_name='intialtor_set')
      reciever =  models.ForeignKey(UserProfile,related_name='reciever_set')
      pending = models.BooleanField(default=True)      
      createddate = models.DateTimeField(auto_now_add=True)
      updateddate = models.DateTimeField(auto_now=True)
      
      
      def __unicode__(self):
        return " Initiator = %s Reciever %s pending %s "%(self.initiator.fullname,self.reciever.fullname,self.pending)
        
      
      @models.permalink
      def get_pending_absolute_url(self):                
              return ('pendingconnectionurl',(),{})
          
      def getfullurl(self,institute):
          ''' brings entire url with the domain name '''
          url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,self.get_pending_absolute_url())
          return url     
          
      
      
      
      
    

