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
from django.db.models import Q


import calendar
import datetime
import logging
import logging.config

from profile.views import getPage
from institution.models import deliverEmail

from institution.models import UserProfile
from connections.models import Connection

mlogger = logging.getLogger(__name__)



@login_required(redirect_field_name='next')
def displayConnections(request):
    mlogger.debug("Display user connections...................")
    profile = request.user.get_profile()
    connections = Connection.objects.filter(Q(pending=False),Q(initiator__id=profile.id)| Q(reciever__id=profile.id) )
  
    #send friends profile
    friends = []
    for conn in connections :
        if conn.initiator.id  ==  profile.id :
            friends.append((conn.reciever,conn.id))
        if conn.reciever.id  ==  profile.id :
            friends.append((conn.initiator,conn.id))            
        
    return render_to_response('connections/connectionhome.html',{'friends':friends},RequestContext(request))
    


@login_required(redirect_field_name='next')
def addConnection(request,touserid):    
    d={}
    try: 
        mlogger.debug("Add new connections...................")
        touserid = int(touserid)
        profile = User.objects.get(pk=int(touserid)).get_profile()
        try :
            Connection.objects.get(initiator__id=request.user.get_profile().id,reciever__id=profile.id)
        except Connection.DoesNotExist :    
            c = Connection()
            c.initiator = request.user.get_profile()
            c.reciever = profile
            c.save()
            #send email to the ereciever
            fullpendingurl = c.getfullurl(request.institute)
            deliverEmail('new_connection_subject.html','new_connection_message.html',{'institute':request.institute,'initiator':c.initiator,'reciever':c.reciever,'fullpendingurl':fullpendingurl},[c.reciever.user.email])
    except :
        d['error'] = "Oops...........some problem at the server"    
    
    json = simplejson.dumps(d)
    return HttpResponse(json)  
    
    
    

@login_required(redirect_field_name='next')
def deleteConnection(request,connectionid):    
    d={}
    d['connectionid'] = connectionid
    try:
        mlogger.debug("Delete connection...................")
        connectionid = int(connectionid)
        Connection.objects.get(pk=connectionid).delete()
    except :
        d['error'] = "OOps...........some problem at the server"
     
    json = simplejson.dumps(d)
    return HttpResponse(json)
    


@login_required(redirect_field_name='next')
def acceptConnection(request,connectionid):
    mlogger.debug("Accepted connection...................")
    d={}
    d['connectionid'] = connectionid
    try:
        mlogger.debug("Delete connection...................")
        connectionid = int(connectionid)
        c = Connection.objects.get(pk=connectionid)
        c.pending=False
        c.save()
    except :
        d['error'] = "OOps...........some problem at the server"
     
    json = simplejson.dumps(d)
    return HttpResponse(json)


@login_required(redirect_field_name='next')
def pendingConnections(request):
    mlogger.debug("Pending connections.................")
    mlogger.debug("Display user connections...................")
    profile = request.user.get_profile()
    connections = Connection.objects.filter(Q(pending=True),Q(reciever__id=profile.id) )
    
    #send friends profile
    friends = []
    for conn in connections :   
        friends.append((conn.initiator,conn.id))            
        
    return render_to_response('connections/pendingconnections.html',{'friends':friends},RequestContext(request))
  




