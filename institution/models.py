from django.db import models
from django.contrib.auth.models import User
import settings
import os
import threading

import logging
import logging.config
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from location.models import Country
import tagging

from statistics.models import Industry,Market





mlogger = logging.getLogger(__name__)

''' Every thing in alumclub surronds under
    Institue ,Faculty , Student
    Bother Sudent and Faculty are alumini of the institutes '''


class Institution(models.Model):
    name = models.CharField(max_length=1024)   
    website = models.URLField(null=True,blank=True)
    phoneno = models.CharField(max_length=20)
    admin  = models.ForeignKey(User)    
    description = models.TextField(null=True,blank=True)    
    #This is the subdomain name
    subdomain = models.CharField(max_length=30,unique=True)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    #Only after cross checking the institutes references we will
    #authenticate the institute    
    active    = models.BooleanField(default=False)
  
    
    def __unicode__(self):
        return "Institution Name = %s " %(self.name,)
        
    
    def get_absolute_url(self):
        return "http://%s.%s" %(self.subdomain,settings.DOMAIN_NAME)
        
        
    def getInstituteFeedUrl(self):
         ''' get the blog feed '''
         url =  "latest/%s" % self.subdomain
         feedurl = reverse("institute_feed_url",kwargs={'url':url})
         return feedurl
        
        
    def getFacultyFeed(self):
        ''' get faculty research Blog Feed'''
        url =  "latest/%s/%s" % (self.subdomain,slugify(self.fullname))
        feedurl = reverse("institute_feed_url",kwargs={'url':url})
        return feedurl
    
    def getInstituteHomeUrl(self):
          ''' brings entire url with the domain name '''
          url =  "http://%s%s/" %(self.subdomain.strip(),settings.DOMAIN)
          return url   
        
        
 
 
def photo_file_path(instance=None, filename=None ):
    user = instance.user
    return os.path.join("images",user.username,filename)
    
 
 

# Create your models here.

class UserProfile(models.Model):
    ''' to note down additional parameter of an user'''
    #one to one relation ship with User and UserProfile
    user = models.ForeignKey(User, unique=True)
    isadmin = models.BooleanField(default=False)    
    personalsite = models.URLField(null=True,blank=True)
    isFaculty = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    fullname = models.CharField(max_length=50)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)  
    #Every memeber who is joining the alumini required memeber approval        
    approved = models.IntegerField(default=0)
    photo = models.ImageField(max_length=1024, upload_to=photo_file_path, blank=True ,null=True )
    country = models.ForeignKey(Country,null=True,blank=True)
    emailverified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=100,default='',null=True,blank=True)    
    state = models.CharField(max_length=25,null=True,blank=True)
    city = models.CharField(max_length=25,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    institutes = models.ManyToManyField(Institution)
    logincount = models.IntegerField(default=0,null=True,blank=True)
    profilepercent = models.FloatField(null=True,blank=True)
        
    
    def getAddress(self):        
        address = ""
        if self.address :
            address = address + self.address +"<br/>"
            
        if self.city :
            address = address + self.city + ","
        if self.state :
            address = address + self.state + ","
        if self.country :
            address = address + self.country.name + ","
            
        return address                
   
    
    def getImage(self):
        ''' return image if it exists otherwise returns a default image'''      
        if len(self.photo.name) == 0  :
            if self.isadmin :
                return settings.DEFAULT_IMAGE
            else :
                return settings.DEFAULT_IMAGE
        else:
            return self.photo
        
    def didHeUploadPhoto(self):
        ''' True if he uploads photograph False if he does not '''
        if len(self.photo.name) == 0  :
            return False
        else :
            return True
        
    @models.permalink
    def get_absolute_url(self):
        return ('profileurl2',(),{'userid': self.user.id})
        
    
    def getNCountryName(self):
        return self.country.replace(" ","_")
        
    def getSlugifyName(self):
        return slugify(self.fullname)
     
    def __unicode__(self):
        if self.isFaculty :
            return " Name = %s , email = %s  %s"% (self.fullname,self.user.email,'faculty')
        elif self.isStudent:
            return " Name = %s , email = %s  %s"% (self.fullname,self.user.email,'student')
        else:
            return " Name = %s , email = %s  %s"% (self.fullname,self.user.email,'admin')
            
            
    def getTags(self):
        plaintext = []
        
        for tag in self.tags :
            plaintext.append(tag.name)
        
        return " ".join(plaintext)
        
    
    @models.permalink
    def get_activation_absolute_url(self):                
            return ('activationurl',(),{'userid':self.user.id,'activation_key':self.activation_key})
          
    def get_full_activation_url(self,institute):
          ''' brings entire url with the domain name '''
          url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,self.get_activation_absolute_url())
          return url     
       
try :
    tagging.register(UserProfile)
except tagging.AlreadyRegistered :
    pass  
    
 
 

class Faculty(models.Model):                 
      institutes = models.ManyToManyField(Institution,through='FacultyInstitute')      
      profile = models.ForeignKey(UserProfile, unique=True)
      createddate = models.DateTimeField(auto_now_add=True)
      updateddate = models.DateTimeField(auto_now=True)
      
      def __unicode__(self):
        return "Faculty Name = %s , email = %s" % (self.profile.user.username,self.profile.user.email)

        
            
class Department(models.Model):
    name = models.CharField(max_length=512)
    established = models.IntegerField(null=True,blank=True)
    institute = models.ForeignKey(Institution)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
    
    def __unicode__(self):
        return "%s" %(self.name)
        
        
class Course(models.Model):
    name = models.CharField(max_length=512)
    introduced = models.IntegerField(null=True,blank=True)    
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    departments = models.ManyToManyField(Department)
    institute = models.ForeignKey(Institution)
    user = models.ForeignKey(User)
    
    
    def __unicode__(self):
        return "%s" %(self.name)
        
    
        
class Degree(models.Model):
    name = models.CharField(max_length=120)
    established = models.IntegerField(null=True,blank=True)
    institute = models.ForeignKey(Institution)
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
    
    def __unicode__(self):
        return "%s" %(self.name)
        
    
    
    
    
    
    
                
    

class FacultyInstitute(models.Model):
      ''' a faculty can be an alumini for multiple institutes'''       
      faculty = models.ForeignKey(Faculty)
      institute = models.ForeignKey(Institution)
      joineddate = models.DateTimeField(auto_now_add=True)
      lastupdate = models.DateTimeField(auto_now=True)
      subjects = models.TextField()
      specialization = models.CharField(max_length=255,null=True,blank=True)
      designation = models.CharField(max_length=200,null=True,blank=True)
      department = models.ForeignKey(Department,null=True,blank=True)      
      
      def getSimpleProfile(self):
         return "%s , %s " %(self.designation,self.department.name)
         
      def getBatch(self):         
          return "  "     
      
 
      
class Student(models.Model):       
      #various constants
      STUDENT = 'student'
      EMPLOYMENT = 'employee'
      #business owner
      BOWNER = 'owner'
      LOOKINGFORWORK = 'lwork'
      FREELANCE = 'freelance'
      
      #tuple (databasevalue,displayvalue)
      WHAT_DOING = (
        ( STUDENT  , 'iam a student'),
	( EMPLOYMENT , 'Employed' ),
	( BOWNER , 'A Business Owner'),	
	( LOOKINGFORWORK,'Looking for Work'),
        ( FREELANCE,'Working Independently'),
       )
  
      #institutes in which he is an alumini
      institutes = models.ManyToManyField(Institution,through='StudentInstitute')           
      #Employment details
      whatiamdoing = models.CharField(max_length=50,choices=WHAT_DOING,null=True,blank=True)
      company = models.CharField(max_length=200,null=True,blank=True)
      title = models.CharField(max_length=250,null=True,blank=True)
      industry = models.ForeignKey(Industry,null=True,blank=True)
      market = models.ForeignKey(Market,null=True,blank=True)  
      profile = models.ForeignKey(UserProfile, unique=True)
      createddate = models.DateTimeField(auto_now_add=True)
      updateddate = models.DateTimeField(auto_now=True)
  
      
      def __unicode__(self):
        return "Student Name = %s , email = %s" % (self.profile.fullname,self.profile.user.email)
        
         
            
      
      
      
class StudentInstitute(models.Model):
    ''' A student can be alumini of multiple institutes '''
    student = models.ForeignKey(Student)
    institute = models.ForeignKey(Institution)
    joineddate = models.DateTimeField(auto_now_add=True)
    lastupdate = models.DateTimeField(auto_now=True)
    fromyear =  models.IntegerField()
    toyear = models.IntegerField(null=True,blank=True)
    #what you did there
    #course and department
    course = models.ForeignKey(Course)
    department = models.ForeignKey(Department)
    degree = models.ForeignKey(Degree)    
    
    def getSimpleProfile(self):        
        if self.student.whatiamdoing == "employee" :
            return "%s , %s " %(self.student.title,self.student.company)
        elif self.student.whatiamdoing == "owner":
            return "owner at %s  " %(self.student.company,)
        else :
            return ""
            
    
    def getBatch(self):         
        if self.toyear is None:
            return "%s -  "%(self.fromyear,)
        else:
            return "%s - %s"%(self.fromyear,self.toyear)
  

              
''' Thread which delivers the emails to users '''
class DevEmailThread(threading.Thread):  
       def __init__(self,subject_template,message_template,context,email):           
            self.subject_template = subject_template
            self.message_template = message_template
            self.context = context
            self.email = email            
            threading.Thread.__init__(self)  
              
       def run (self):           
            subject_template = self.subject_template
            message_template = self.message_template 
            context = self.context
            email = self.email
            subject_file_name = "institution/emails/%s"%(subject_template,)
            message_file_name = "institution/emails/%s"%(message_template,) 
            subject = render_to_string(subject_file_name,context)
            message = render_to_string(message_file_name,context)            
            mlogger.debug("Subject = %s message = %s " % (subject,message))
           
            if type(email) == type([]) :
                for everyemail in email :
                    mlogger.debug("sending an email to %s .............." % (everyemail,))                    
                    msg = EmailMessage(subject,message, settings.EMAIL_HOST_USER, [everyemail])
                    msg.content_subtype = "html"
                    msg.send()
            else:
                mlogger.debug("sending an email to %s .............." % (email,))
                msg = EmailMessage(subject,message, settings.EMAIL_HOST_USER, [email])
                msg.content_subtype = "html"
                msg.send()
    
           

def deliverEmail(subject_template,message_template,context,email):
        ''' Delivering email  '''
        mlogger.debug("Delivering email..................")        
        #start a thread which handles these notifications
        DevEmailThread(subject_template,message_template,context,email).start()
        



        
        
        
        
        
        
  
def performProfilesave(profile):
    mlogger.debug("performing profile saves.....................")
    if profile.isStudent :
        try :
            student = Student.objects.get(profile__id = profile.id)
            performSIsaves(student)
        except Student.DoesNotExist :
            pass                    
    elif profile.isFaculty :
        try:
            faculty = Faculty.objects.get(profile__id = profile.id)
            performFIsaves(faculty)
        except Faculty.DoesNotExist :
            pass            
    

def performSIsaves(student):    
    ''' perform student institute saves'''
    mlogger.debug("performing student institute saves.......................")
    silist = StudentInstitute.objects.filter(student__id = student.id)
    for si in silist :
            si.save() 
    

def performFIsaves(faculty):
    ''' perform faculty institute saves'''
    mlogger.debug("performing faculty institute saves.......................")
    filist = FacultyInstitute.objects.filter(faculty__id = faculty.id)
    for fi in filist :
            fi.save()
            
            

      
        
#setup signals which helps us to update the index properly
def trigger_index_change(sender, instance, created, **kwargs):
    mlogger.debug("triggering index change...................")
    
    if instance.__class__.__name__ == 'User':
        try :
            profile = instance.get_profile()
            performProfilesave(profile)
        except :
            pass        
    elif instance.__class__.__name__ == 'UserProfile' :
        profile = instance
        performProfilesave(profile)
    elif instance.__class__.__name__ == 'Student' :
        performSIsaves(instance)               
    elif instance.__class__.__name__ == 'Faculty' :
        performFIsaves(instance)       
        
    
                
    


signals.post_save.connect(trigger_index_change, sender=User)
signals.post_save.connect(trigger_index_change, sender=UserProfile)
signals.post_save.connect(trigger_index_change, sender=Student)
signals.post_save.connect(trigger_index_change, sender=Faculty)


        
        
        
        
        
        
     
      
    
    
    
    