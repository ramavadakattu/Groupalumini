from django.db import models
from institution.models import Department,Course,Institution ,UserProfile ,StudentInstitute,FacultyInstitute
from location.models import Country,State
from statistics.models import Industry,Market
from django.contrib.auth.models import User

import logging
import logging.config


mlogger = logging.getLogger(__name__)


class MailGroup(models.Model):
        name = models.CharField(max_length=200)
        alumini = models.BooleanField(default=False)
        faculty = models.BooleanField(default=False)
        department = models.ForeignKey(Department,null=True,blank=True)
        fdepartment = models.ForeignKey(Department,null=True,blank=True,related_name="fdepartment_set")
        program = models.ForeignKey(Course,null=True,blank=True)        
        passoutyear = models.IntegerField(null=True,blank=True)
        country  = models.ForeignKey(Country,null=True,blank=True)
        fcountry  = models.ForeignKey(Country,null=True,blank=True,related_name="fcountry")
        industry = models.ForeignKey(Industry,null=True,blank=True)
        market = models.ForeignKey(Market,null=True,blank=True)
        entirealumini = models.BooleanField(default=False)
        createddate = models.DateTimeField(auto_now_add=True)
        updateddate = models.DateTimeField(auto_now=True)
        user = models.ForeignKey(User)        
        institute  = models.ForeignKey(Institution)
        
        
        def getEmailList(self,institute) :
            ''' returns the emaillist after examining the constraints posed by this group '''
            emaillist = []
            if self.entirealumini : 
                emaillist = UserProfile.objects.filter(institutes__in=[institute.id]).values_list('user__email',flat=True)
            else :
                #get the alumini mailing list                
                if self.alumini:
                    si = StudentInstitute.objects.filter(institute__id=institute.id)                    
                    if self.department :
                         si = si.filter(department__id=self.department.id)
                    if self.program :
                        si = si.filter(course__id=self.program.id)
                    if self.industry :
                        si = si.filter(student__industry__id=self.industry.id)
                    if self.market :
                        si = si.filter(student__market__id=self.market.id)                                 
                    if self.passoutyear :
                        si = si.filter(toyear=self.passoutyear)
                    if self.country :
                        si = si.filter(student__profile__country__id=self.country.id)
                        
                    aluminilist = si.values_list('student__profile__user__email',flat=True)
                    mlogger.debug("emaillist = %s" % (str(aluminilist),))
                    emaillist = emaillist + list(aluminilist)
                    
                if self.faculty:
                    fi = FacultyInstitute.objects.filter(institute__id=institute.id)
                    if self.fdepartment :
                         fi = fi.filter(department__id=self.fdepartment.id)
                         
                    if self.fcountry :
                         fi = fi.filter(faculty__profile__country__id=self.fcountry.id)
                         
                    facultylist = fi.values_list('faculty__profile__user__email',flat=True)
                    emaillist = emaillist + list(facultylist)
                    mlogger.debug("Faculty list = %s" % (str(facultylist),))
                    
            return emaillist
        
            
        def __unicode__(self):
            return "%s"%(self.name,)
            
            
            
        
        
        
        
    
    
    

