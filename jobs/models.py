from django.db import models
from django.contrib.auth.models import User

from institution.models import Institution
from django.utils.html import linebreaks , strip_tags ,escape , urlize

from mailgroups.models import MailGroup
import settings
import tagging
# Create your models here.


class Job(models.Model):
    postedby = models.ForeignKey(User,null=True,blank=True)
    institute = models.ForeignKey(Institution,null=True,blank=True)
    title = models.CharField(max_length=567)
    description = models.TextField()
    location = models.CharField(max_length=50,null=True,blank=True)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    sendemail = models.ForeignKey(MailGroup,null=True,blank=True)
    viafeed = models.BooleanField(default=False)
    viafeeddatetime = models.DateTimeField(null=True,blank=True)
    
    @models.permalink
    def get_absolute_url(self):                
            return ('viewjoburl',(),{'jobid': self.id})
          
    def getfullurl(self,institute):
        ''' brings entire url with the domain name '''
        url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,self.get_absolute_url())
        return url
    
    
try :
    tagging.register(Job)
except tagging.AlreadyRegistered :
    pass      
        
        
        
        
class JobComment(models.Model):
    job = models.ForeignKey(Job)   
    text = models.TextField()
    postedby = models.ForeignKey(User)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return "%s "%(self.text[:200],)
     
    def getNText(self,ajax=False):        
        ntext = self.text.strip()
        ntext = strip_tags(ntext)
        ntext = ntext.strip()
        
        ntext = escape(ntext)
        ntext = urlize(ntext)   
        return ntext.replace("\n","<br/>")
            
        
        
        
    
        
    
