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
from clubcalendar import InsituteCalendar

import calendar
import datetime
import logging
import logging.config

from profile.views import getPage

from events.models import Event , EventAttendance
from events.forms import EventForm
from datetime import datetime

from django.utils.safestring import mark_safe
from institution.models import UserProfile
from institution.models import deliverEmail

from askalumini.views import removeUserTagWeights , assignUserTagWeights


mlogger = logging.getLogger(__name__)

@login_required(redirect_field_name='next')
def getCalendarView(request,month=None,year=None):
    mlogger.debug("Returning the calendar view................")
    today = datetime.now().date()
    if year is None :
        year = today.year
        month = today.month           		
    events = Event.objects.filter(institute__id=request.institute.id,when__year= year,when__month=month)	
    cal = InsituteCalendar(events).formatmonth(int(year), int(month))    
    d = getMonthNames(int(month),int(year))    
    return render_to_response('events/calendar_display.html', {
		'nextmonth':(d['next'],d['nexturl']),
		'prevmonth':(d['prev'],d['prevurl']),
		'currentmonth':(d['current'],d['currenturl']),			
		'calendar': mark_safe(cal)},RequestContext(request))    

	
	
def getMonthNames(themonth,theyear) :
	''' this i think has to do in more pythonic way'''	
        prevmonth = ''
	nextmonth = ''
	curmonth = ''
	cururl = ''
	prevurl =''
	nexturl = ''
	
	curmonth = calendar.month_name[themonth]+str(theyear)
	cururl =  reverse("calendarviewurl2", kwargs={"year":theyear,"month":themonth})
	
	
	if themonth == 1:
	   prevmonth = calendar.month_name[12]+str(theyear-1)
	   prevurl =  reverse("calendarviewurl2", kwargs={"year":theyear-1,"month":12})
	   nextmonth = calendar.month_name[themonth+1]+str(theyear)
	   nexturl =  reverse("calendarviewurl2", kwargs={"year":theyear,"month":themonth+1})	   
	elif themonth == 12:
	   nextmonth = calendar.month_name[1]+str(theyear+1)
	   nexturl =  reverse("calendarviewurl2", kwargs={"year":theyear+1,"month":1})
	   prevmonth = calendar.month_name[themonth-1]+str(theyear)
	   prevurl =  reverse("calendarviewurl2", kwargs={"year":theyear,"month":themonth-1})
	   
	else :
	   nextmonth = calendar.month_name[themonth+1]+str(theyear)
	   nexturl =  reverse("calendarviewurl2", kwargs={"year":theyear,"month":themonth+1})
	   prevmonth = calendar.month_name[themonth-1]+str(theyear)
	   prevurl =  reverse("calendarviewurl2", kwargs={"year":theyear,"month":themonth-1})
	   
	   
	d= {}
	d['current'] = curmonth
	d['currenturl'] = cururl
	d['next'] = nextmonth
	d['nexturl'] = nexturl
	d['prev'] = prevmonth
	d['prevurl'] = prevurl
	
	return d


@login_required(redirect_field_name='next')
def getAgendaView(request):
    mlogger.debug("Display ")    
    page = getPage(request)
    today = datetime.now().date()   
    events = Event.objects.filter(institute__id=request.institute.id,when__gte=today).order_by('when')
    return object_list(request, queryset=events,
                           extra_context={},template_object_name="event",paginate_by=settings.EVENTS_PER_PAGE,page=page,template_name="events/agenda_display.html")
 


   
@login_required(redirect_field_name='next')    
def createEvent(request):
    mlogger.debug("Create new event ..........................")
    if request.method == "GET":
        form = EventForm(user=request.user)
        return render_to_response('events/create_event.html',{'form':form},RequestContext(request))        
    elif request.method == "POST" :
        form = EventForm(request.POST,user=request.user)        
        if form.is_valid() :
            event = form.save(commit=False)
            event.user = request.user
            event.institute = request.institute
            event.save()
            
            event.tags = form.cleaned_data['tags']
            assignUserTagWeights(event.tags,request.user,settings.CONTRIBUTION_WEIGHT)
            
            if event.sendemail is not None :
                emaillist = event.sendemail.getEmailList(request.institute)                
                deliverEmail('event_created_subject.html','event_created.html',{'institute':request.institute,'event':event,'edit':False,'site':settings.SITE_URL},emaillist)
                
            create_message(request,"Succesfully created the event ...............")
            return HttpResponseRedirect(reverse('agendaviewurl'))               
    return render_to_response('events/create_event.html',{'form':form},RequestContext(request))                
      
      
def getInstituteEmailList(institute):    
    emaillist = UserProfile.objects.filter(institutes__in = [institute.id]).values_list('user__email',flat=True)
    return list(emaillist)
    
    
        
    
@login_required(redirect_field_name='next') 
def viewEvent(request,eventid):
    mlogger.debug("viewing the event %s "%(eventid,))
    eventid = int(eventid)
    event = Event.objects.get(pk=eventid)
    if request.user.id != event.user.id  :
        assignUserTagWeights(event.tags,request.user,settings.VIEW_WEIGHT)          
    if  list(EventAttendance.objects.filter(user__id=request.user.id,event__id=eventid,institute__id=request.institute.id)) :
        attending = True
    else :
        attending = False
    return render_to_response('events/viewevent.html',{'event':event,'attending':attending},RequestContext(request))    

@login_required(redirect_field_name='next')    
def editEvent(request,eventid):
    eventid = int(eventid)
    event = Event.objects.get(id=eventid)
    originaltags = event.tags
    if request.user.id == event.user.id :
        if request.method == "GET" :
            mlogger.debug("the person who posted the event is editing")
            form = EventForm(instance=event,initial={'tags':' '.join(event.tags.values_list('name',flat=True))},user=request.user)            
            return render_to_response('events/create_event.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
            form = EventForm(request.POST,instance=event,user=request.user)
            if form.is_valid() :
                   newevent = form.save(commit=False)
                   newevent.save()                   
                   removeUserTagWeights(originaltags,request.user,settings.CONTRIBUTION_WEIGHT)
                   newevent.tags = form.cleaned_data['tags']
                   assignUserTagWeights(newevent.tags,request.user,settings.CONTRIBUTION_WEIGHT)               
                   if event.sendemail is not None :
                        emaillist = event.sendemail.getEmailList(request.institute)                          
                        deliverEmail('event_created_subject.html','event_created.html',{'institute':request.institute,'event':event,'edit':True,'site':settings.SITE_URL},emaillist)
                    
                   create_message(request,"Successfuly edited the event")
                   return HttpResponseRedirect(reverse('agendaviewurl')) 
            else:      
                   return render_to_response('events/create_event.html',{'form':form,'editmode':True},RequestContext(request))  
            
    else :
        create_message(request,"You are not authorized to edit this event")
        return HttpResponseRedirect(reverse('agendaviewurl'))
        

@login_required(redirect_field_name='next')  
def deleteEvent(request,eventid):
    eventid = int(eventid)
    event = Event.objects.get(id=eventid)
    removeUserTagWeights(event.tags,request.user,settings.CONTRIBUTION_WEIGHT)
    event.delete()
    create_message(request,"Successfuly deleted the event................")
    return HttpResponseRedirect(reverse('agendaviewurl'))
    
    

    
def trackAttendence(request,eventid,attendingflag):   
    d = {}
    attendingflag = int(attendingflag)
    event = Event.objects.get(pk=int(eventid))
    
   
    if attendingflag > 0 :        
        #event.peopleattending.add(request.user)        
        #Tracking event attendance
        ea  = EventAttendance()
        ea.user = request.user
        ea.institute = request.institute
        ea.event = event
        ea.save()
                
        d['attending'] = 1
        d['spancontent'] = "<span> <a href='%s'> %s </a> </span>," %(request.user.get_profile().get_absolute_url(),request.user.get_profile().fullname)
    else :
        EventAttendance.objects.filter(user__id=request.user.id,event__id=eventid,institute__id=request.institute.id).delete()
        d['attending'] = 0
     
    
    d['error'] = "success"
    d['eventid'] = int(eventid)    
    d['totalcount'] = event.peopleattending.count() 
    json = simplejson.dumps(d)         
    return HttpResponse(json)       
        
        
        
    
    
    
    




