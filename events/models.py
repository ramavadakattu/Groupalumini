#google.com
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import linebreaks , strip_tags ,escape , urlize

from institution.models import Institution
from mailgroups.models import MailGroup

import tagging

# Create your models here.

class Event(models.Model):    
    user = models.ForeignKey(User)
    institute = models.ForeignKey(Institution)
    what = models.CharField(max_length=1024)
    when = models.DateField()
    where = models.CharField(max_length=512)
    starttime = models.TimeField()
    duration = models.IntegerField()
    durationtag = models.CharField(max_length=124,choices=[('dummy','dummy')])
    description = models.TextField(null=True,blank=True)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    peopleattending = models.ManyToManyField(User,related_name="attendingevents",through="EventAttendance")
    sendemail = models.ForeignKey(MailGroup,null=True,blank=True)
    
    
    
    def __unicode__(self):
        return "what = %s when= %s start_time = %s "%(self.what,str(self.when),str(self.starttime))
        
        
    def getNDescription(self):
        if self.description is not None :
            ntext = self.description.strip()
            ntext = strip_tags(ntext)
            ntext = ntext.strip()            
            ntext = escape(ntext)
            ntext = urlize(ntext)   
            return ntext.replace("\n","<br/>")
            
            
    @models.permalink
    def get_absolute_url(self):
        return ('vieweventurl',(),{'eventid': self.id})
        
    
    def getTime(self):
       return  self.starttime.strftime("%I:%M %p")
       
    def getTotalAttending(self):       
        return len(list(EventAttendance.objects.filter(event__id=self.id)))
        

    def clean_tags(self):
            mlogger.debug("Make sure it contatins only alpahnumeric characters")
            tags = self.cleaned_data['tags'].strip()    
            #make sure that the tags are of valid string
            if len(tags) == 0 :
              return self.cleaned_data['tags']
              
            #if he enters any things make sure it contains only alpha numeric characters            
            e = re.compile(r"[0-9A-Za-z-. ]+",re.IGNORECASE)
            result = e.match(tags)    
            if result is not None  and len(tags) == result.span()[1] :
              return self.cleaned_data['tags']
            else :
              raise forms.ValidationError("Error:Tags should only contain alphanumeric characters, space,hypen('-'),dot('.'). Tags shoud be saperated by space")
         
   
    
try :
    tagging.register(Event)
except tagging.AlreadyRegistered :
    pass      
        
                 
            
class EventAttendance(models.Model):
    ''' An entry here represents user is attending the event'''
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    institute = models.ForeignKey(Institution)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return "User %s is attending the event %s"%(self.user.get_profile().fullname,self.event.what)
        
        
    
    
    
