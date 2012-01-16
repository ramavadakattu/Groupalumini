from django.db import models
from institution.models import Institution
from django.contrib.auth.models import User
from django.utils.html import linebreaks , strip_tags ,escape , urlize
from mailgroups.models import MailGroup
import settings
import tagging



class Entry(models.Model):        
    headline = models.CharField(max_length=1024)    
    content = models.TextField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    institute = models.ForeignKey(Institution)
    #All the things which faculty published comes under research paper
    research_paper = models.BooleanField(default=False)
    sendemail = models.ForeignKey(MailGroup,null=True,blank=True)
    user = models.ForeignKey(User)
    

    def __unicode__(self):
        return self.headline
    
    @models.permalink
    def get_absolute_url(self):        
        if self.research_paper :
            return ('singlepaperurl',(),{'entry_id': self.id})
        else:
            return ('singleposturl',(),{'entry_id': self.id})
            
                
    def getfullurl(self,institute):
        ''' brings entire url with the domain name '''
        url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,self.get_absolute_url())
        return url


try :
    tagging.register(Entry)
except tagging.AlreadyRegistered :
    pass  
    
    
    
class Comment(models.Model):
    entry =  models.ForeignKey(Entry)
    text = models.TextField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)   
    user = models.ForeignKey(User,related_name="blogcomments",null=True,blank=True)
    nouser = models.BooleanField(default=False)
    username = models.CharField(max_length=56,null=True,blank=True)
    webaddress = models.CharField(max_length=1024,null=True,blank=True)
    
    
    def __unicode__(self):
        return self.text
    
    
    def getNText(self):        
        ntext = self.text.strip()
        ntext = strip_tags(ntext)
        ntext = ntext.strip()
        
        ntext = escape(ntext)
        ntext = urlize(ntext)   
        return ntext.replace("\n","<br/>")
    
    

   