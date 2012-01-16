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

from django.views.generic.list_detail import object_list
from mailgroups.models import MailGroup
from mailgroups.forms import MailGroupForm
from statistics.models import Industry

from profile.views import getPage# Create your views here.

mlogger = logging.getLogger(__name__)




def displayMailGroups(request):
    mlogger.debug("display mail groups....................")
    mailgroups = MailGroup.objects.filter(user__id=request.user.id)
    #if there not entire alumini mai group let us create for him
    egroup =  MailGroup.objects.filter(user__id=request.user.id,entirealumini=True)
    if egroup :
        pass
    else :
        mg = MailGroup()
        mg.name = "Entire Alumini"
        mg.user = request.user
        mg.institute = request.institute
        mg.entirealumini = True
        mg.save()            
    return render_to_response('mailgroups/mailgrouphome.html',{'mailgroups':mailgroups},RequestContext(request))


def createMailGroup(request):
    mlogger.debug("create new mail group......................")
    industries = Industry.objects.all()
    if request.method == "GET" :
        form = MailGroupForm(institute=request.institute)        
        return render_to_response('mailgroups/createmailgroup.html',{'form':form,'industries':industries},RequestContext(request))
    else :
        form=MailGroupForm(request.POST,institute=request.institute)       
        if form.is_valid() :            
            mailgroup = form.save(commit=False)
            mailgroup.user = request.user
            mailgroup.institute = request.institute
            #assert False            
            mailgroup.save()
            create_message(request,"Successfully created mail group")
            return HttpResponseRedirect(reverse('displaymailgroupurl'))                          
        else :
            return render_to_response('mailgroups/createmailgroup.html',{'form':form,'industries':industries},RequestContext(request))
            
        
    
def deleteMailGroup(request,mailgroupid):
    mlogger.debug("deleted a mail group...........................")
    MailGroup.objects.get(pk=mailgroupid).delete()
    create_message(request,"Successfully deleted mail group")
    return HttpResponseRedirect(reverse('displaymailgroupurl'))                          
    
    
    
def editMailGroup(request,mailgroupid):
    mlogger.debug("edit a mail group................................")
    mailgroupid = int(mailgroupid)
    mailgroup = MailGroup.objects.get(pk=mailgroupid)
    industries = Industry.objects.all()
    if request.user.id == mailgroup.user.id :
        if request.method == "GET" :
            mlogger.debug("the person who posted the job is editing")
            form = MailGroupForm(instance=mailgroup,institute=request.institute)            
            return render_to_response('mailgroups/createmailgroup.html',{'form':form,'editmode':True,'industries':industries},RequestContext(request))
        elif request.method == "POST":            
            form = MailGroupForm(request.POST, instance=mailgroup , institute=request.institute)
            if form.is_valid() :
                form.save()
                create_message(request,"Successfuly edited the mailgroup")
                return HttpResponseRedirect(reverse('displaymailgroupurl'))
            else:
                return render_to_response('mailgroups/createmailgroup.html',{'form':form,'editmode':True,'industries':industries},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this mailgroup")
        return HttpResponseRedirect(reverse('displaymailgroupurl'))                          
        
    
    
