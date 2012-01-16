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


from institution.models import deliverEmail
from askalumini.models import Question,Answer,Comment
from askalumini.forms import QuestionForm,AnswerForm
from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , photo_file_path
from profile.models import ShortMessages
from django.views.generic.list_detail import object_list

from django.utils.html import linebreaks , strip_tags ,escape , urlize


mlogger = logging.getLogger(__name__)
# Create your views here.


@login_required(redirect_field_name='next')  
def locateHome(request):
    mlogger.debug("locating alumini......................")
    #get the last 100 people who are registered in this institute
    mlogger.debug("Which institute = %s"%(request.institute,))    
    peoplezip = getPeople(request.institute)    
    countryzip = getTotalByCountry(request.institute)   
    level = "country"
    address = None
    count =  UserProfile.objects.filter(isadmin=False,country__isnull=False,state__isnull=False,institutes__in=[request.institute.id]).count()    
    return render_to_response("location/locate.html",{'peoplezip':peoplezip,'countryzip':countryzip,'level':level,'address':address,'count':count},RequestContext(request))
    
    

 
def getTotalByCountry(institute):    
    #fetch the non unique countries
    
    countries = UserProfile.objects.filter(isadmin=False,institutes__in=[institute.id],country__isnull=False).values_list('country__name', flat=True).distinct()
    
    countries = list(countries)    
    
    
    noofpeople = []
    for country in countries :        
            noofpeople.append(len(UserProfile.objects.filter(isadmin=False,institutes__in=[institute.id],country__name__iexact=country)))
        
    
    return zip(countries,noofpeople)
    
@login_required(redirect_field_name='next')     
def browseByCountry(request,ncountryname):    
    country = ncountryname.replace("-"," ")
    if request.method == "POST" :        
        d={}
        try:
                message = request.POST['text']
                message = convertToProperHTML(message)
                #emails of all people living inthis country are
                emails =  UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country).values_list('user__email', flat=True).distinct()                
                deliverEmail('country_wide_subject.html','country_wide_message.html',{'institute':request.institute,'message':message,'sourceuser':request.user,'countrywide':True,'statewide':False},list(emails))
        except :
                d['error'] = "oops........some problem at the server end"
                
        json = simplejson.dumps(d)
        return HttpResponse(json)                
        #return HttpResponseRedirect(reverse('countryurl',kwargs={'ncountryname':ncountryname}))
    else :    
        mlogger.debug("country name = %s "% (country,))
        mlogger.debug("getting the state details....................")
        states = UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country).values_list('state', flat=True).distinct()
          
        noofpeople = []
        for state in states :
            noofpeople.append(len(UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country,state__iexact=state)))
        
        statezip = zip(states,noofpeople)
        peoplezip = getPeople(request.institute,country)
        level = "state"
        address = country
        count =  UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country).count()
        return render_to_response("location/locate.html",{'peoplezip':peoplezip,'statezip':statezip,'level':level,'address':address,'country':country,'count':count},RequestContext(request))
        
    
def browseByState(request,ncountryname,nstatename,pageno=None):
       
    mlogger.debug("Browsing the people by state,.......................")
    country = ncountryname.replace("-"," ")
    state = nstatename.replace("-"," ")
    if request.method == "POST" :        
        d={}
        try:
                message = request.POST['text']
                message = convertToProperHTML(message)
                #emails of all people living inthis country are
                emails =  UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country,state__iexact=state).values_list('user__email', flat=True).distinct()                
                deliverEmail('country_wide_subject.html','country_wide_message.html',{'institute':request.institute,'message':message,'sourceuser':request.user,'statewide':True,'countrywide':False},list(emails))
        except :
                d['error'] = "oops........some problem at the server end"
                
        json = simplejson.dumps(d)
        return HttpResponse(json)                
    else:
    
            if pageno is None :
                  pageno = 1
            
            #for  map purposes
            peoplezip = getPeople(request.institute,country,state)
           
            #for display purposes
            paginator = Paginator(UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country,state__iexact=state).order_by("-createddate"),settings.PEOPLE_PER_PAGE)        
            apage = paginator.page(pageno)
            
            #get the corresponding entities for Student Institute ,Faculty Institute
            entities =[]
            for p in apage.object_list :
                profile = p
                if p.isFaculty :
                    f = Faculty.objects.get(profile__id = profile.id )
                    fi = FacultyInstitute.objects.get(faculty__id = f.id,institute__id = request.institute.id)
                    entities.append(fi)
                else:
                    s = Student.objects.get(profile__id = profile.id )
                    si = StudentInstitute.objects.get(student__id = s.id,institute__id=request.institute.id)
                    entities.append(si)
            
            
            peopledisplayzip = zip(apage.object_list,entities)    
            address =  "%s , %s" %(state,country)
            level =  "city"
            count =  UserProfile.objects.filter(isadmin=False,institutes__in=[request.institute.id],country__name__iexact=country,state__iexact=state).count()
            return render_to_response("location/locate.html",{'peopledisplayzip':peopledisplayzip,'peoplezip':peoplezip,'level':level,'address':address,'country':country,'state':state,'pagedetail':apage,'count':count},RequestContext(request))
         
    
    
def getPeople(institute,country=None,state=None):
    mlogger.debug("COuntry = %s"% (country,))
    mlogger.debug("institute = %s"% (institute,))
    mlogger.debug("state = %s"% (state,))
      
    people = []
    if country is not None :
        if state is None :
          people = UserProfile.objects.filter(isadmin=False,institutes__in=[institute.id],country__isnull=False,country__name__iexact=country).order_by("-createddate")[:200]
        else:
          people = UserProfile.objects.filter(isadmin=False,institutes__in=[institute.id],country__isnull=False,country__name__iexact=country,state__iexact=state).order_by("-createddate")[:200]  
    else:        
        people = UserProfile.objects.filter(isadmin=False,country__isnull=False,state__isnull=False,institutes__in=[institute.id]).order_by("-createddate")[:200]
        
    people = list(people)    
    entities =[]
    for p in people :
        profile = p
        
        if profile.latitude is None or profile.longitude is None or profile.country is None :
            people.remove(p)
            
        
        
        if p.isFaculty :
            try:
                f = Faculty.objects.get(profile__id = profile.id )
            except Student.DoesNotExist :
                if p in people :
                    people.remove(p)
                    continue
                else :
                    continue
            fi = FacultyInstitute.objects.get(faculty__id = f.id,institute__id = institute.id)
            entities.append(fi)
        else:
            s = None
            try:
                s = Student.objects.get(profile__id = profile.id )
            except Student.DoesNotExist :
                if p in people :
                    people.remove(p)
                    continue
                else :
                    continue
            si = StudentInstitute.objects.get(student__id = s.id,institute__id=institute.id)
            entities.append(si)
    
    return zip(people,entities)
    
    
def convertToProperHTML(text):
        ntext = text.strip()
        ntext = strip_tags(ntext)
        ntext = ntext.strip()
        
        ntext = escape(ntext)
        ntext = urlize(ntext)   
        return ntext.replace("\n","<br/>")

    
 
    
    
    
