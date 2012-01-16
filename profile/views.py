# Create your views here.
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404
from session_messages import create_message
from django.contrib.auth import authenticate ,login ,logout
import settings
import os
from django.template.loader import render_to_string
from django.contrib.auth.models import UserManager
from django.contrib.auth.views import redirect_to_login
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.utils import simplejson
from django.views.generic.list_detail import object_list

import datetime
import logging
import logging.config


from askalumini.models import Question,Answer,Comment
from askalumini.forms import QuestionForm,AnswerForm
from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , photo_file_path
from connections.models import Connection
from profile.models import ShortMessages
from django.views.generic.list_detail import object_list


mlogger = logging.getLogger(__name__)


@login_required(redirect_field_name='next')
def showProfile(request,userid=None):
    mlogger.debug("display user profile.....................")
    if userid is not None :
        entityuser = User.objects.get(pk=int(userid))
    else :
        entityuser = request.user
        
    profile = entityuser.get_profile()
    
    entity = None
    entitydetail = None
    
    
    #Is ther any potential connection between
    #request.user or entityuser
    connection  = False
    if userid is None :
        connection = True
    else :
        connection = areConnected(request.user,entityuser)
        
    
    if profile.isFaculty :
        entity =  Faculty.objects.get(profile__id=profile.id)
        entitydetail = FacultyInstitute.objects.get(faculty__id = entity.id,institute__id = request.institute.id)
    elif profile.isStudent :
        entity =  Student.objects.get(profile__id=profile.id)        
        entitydetail = StudentInstitute.objects.get(student__id = entity.id,institute__id = request.institute.id)
    elif profile.isadmin :
        #for admin entity and entitydetail is None
        pass       
    
    page = getPage(request)    
    messages = entityuser.messagesrecieved.all().order_by("-createddate")
    
    percentage = getProfilePercentage(request.user,request.institute)
    rnumber = getRoundedValue(percentage)
    image = getProfileIndicatorImage(rnumber)
    noindicator =  False
    
    if percentage == 100 or percentage == 0 :
        noindicator = True
        
    
    return object_list(request,queryset=messages,
                           extra_context={'noindicator':noindicator,'percentage':percentage,'pindicatorimage':image,'connection':connection,'totalcharacters':settings.SHORT_MSG_CHARS,'entityuser':entityuser,'entity':entity,'entitydetail':entitydetail},
                                          template_object_name="message",
                                          paginate_by=settings.PROFILE_MESSAGES,
                                          page=page,template_name="profile/profile.html")        
       
       
def getProfilePercentage(user,institute):
    profile =  user.get_profile()
    percentage = 25
    
    #location and website details
    if profile.personalsite is not None :
        percentage = percentage +5
    
    if profile.country is not None :
        percentage = percentage +5
        
        if profile.state is not None :
            percentage = percentage +5
            
        if profile.city is not None :
            percentage = percentage +5
            
        if profile.address is not None :
            percentage = percentage + 5
            
    #Professional details
    if profile.isStudent :
        student = profile.student_set.all()[0]
        if student.whatiamdoing  is not None :
            percentage = percentage +25
        
        
    if profile.isFaculty :
        faculty = profile.faculty_set.all()[0]
        fi = FacultyInstitute.objects.get(faculty__id = faculty.id,institute__id = institute.id)
        
        if fi.subjects is not None:
            percentage = percentage +5
        
        if fi.specialization is not None:
            percentage = percentage + 10
            
        if fi.designation is not None :
            percentage = percentage +10
            
    return percentage       
       
      

def getRoundedValue(percentage):
    return  int(percentage/10)
    

def getProfileIndicatorImage(number):
    return settings.PROFILE_INDICATOR_IMAGE+str(number)+settings.PROFILE_INDICATOR_EXTENSION




   
def areConnected(user1,user2):
    ''' Utiltity method which says whether two people are connected or not '''    
    profile1 = user1.get_profile()
    profile2 = user2.get_profile()
    
    if profile1.id == profile2.id :
        return True  
    
    result = Connection.objects.filter(initiator__id=profile1.id,reciever=profile2.id,pending=False)
    if result :
        return True
    else :
        result = Connection.objects.filter(initiator__id=profile2.id,reciever=profile1.id,pending=False)
        if result :
            return True
        else :
            return False
        
    
    
def getPage(request):
    '''returns the page number from this request'''
    page = None
    try :
        page = int(request.GET['page'])        
    except KeyError :
        page = 1
        
    return page      
    
    
@login_required(redirect_field_name='next')    
def addShortMessage(request,touserid=None):  
    d = {}
   
    try:
            if request.method == "POST" :        
                fromuser = request.user
                touser = User.objects.get(pk=int(touserid))        
                sm = ShortMessages()
                sm.fromuser = fromuser
                sm.touser = touser
                sm.text = request.POST['text'][:settings.SHORT_MSG_CHARS]
                sm.save()
                ntext = sm.getNText()                
              
                
                if len(ntext) == 0 :
                    d['error'] = "Some problem with the comment"
                else:
                    d['text'] = "%s--<a href=\"%s\"> %s </a>"%(sm.getNText(ajax=True),fromuser.get_profile().get_absolute_url(),fromuser.get_profile().fullname)                  
                    d['name'] = fromuser.get_profile().fullname
    except:
        d['error'] = "oops........some problem at the server end"
    
    json = simplejson.dumps(d)
    return HttpResponse(json)   
        
        
    
    
    
