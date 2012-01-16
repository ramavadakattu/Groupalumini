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
from institution.models import deliverEmail


from askalumini.views import removeUserTagWeights , assignUserTagWeights

from profile.views import getPage

import datetime
import logging
import logging.config



from institution.models import UserProfile

from publish.forms import PublishForm
from publish.models import Entry ,Comment
mlogger = logging.getLogger(__name__)



def displayNewsLetters(request):
    mlogger.debug("Display news letters home...........................")   
    entries = Entry.objects.filter(institute__id=request.institute.id,research_paper=False).order_by('-createddate')
    page = getPage(request)    
    return object_list(request, queryset=entries,
                           extra_context={},template_object_name="entry",paginate_by=settings.ENTRIES_PER_PAGE,page=page,template_name="publish/institute_publish_home.html")
 
@login_required(redirect_field_name='next') 
def publishNewsLetter(request,entry_id=None):
    mlogger.debug("publish new newsletters")
    if request.method == "GET" :
        if entry_id is None :
               form = PublishForm(user=request.user)
        else :
               entry=Entry.objects.get(pk=entry_id)
               form = PublishForm(instance=entry,user=request.user)
        return render_to_response('publish/institute_create_new.html',{'form':form},RequestContext(request))
    elif request.method == "POST" :        
        form = PublishForm(request.POST,user=request.user)
        if form.is_valid() :
            entry = form.save(commit=False)
            entry.institute = request.institute
            entry.user = request.user
            entry.save()
            if request.POST['whichbutton'] == "save" :                
                create_message(request,"saved your news letter")           
                return HttpResponseRedirect(reverse('publishnewurl2',kwargs={'entry_id':entry.id})+"?backto=publishhome")
            else:
                if entry.sendemail is not None :                    
                    emaillist = entry.sendemail.getEmailList(request.institute)
                    fullurl = entry.getfullurl(request.institute)
                    deliverEmail('new_newsletter_subject.html','new_newsletter.html',{'institute':request.institute,'entry':entry,'fullurl':fullurl},emaillist)
                
                entry.tags = form.cleaned_data['tags']
                assignUserTagWeights(entry.tags,request.user,settings.CONTRIBUTION_WEIGHT)
                create_message(request,"Successfully created blog post")
                return HttpResponseRedirect(reverse('newsletterurl'))               
        else:
            return render_to_response('publish/institute_create_new.html',{'form':form},RequestContext(request))            
        
       
@login_required(redirect_field_name='next')       
def editEntry(request,entry_id):
    mlogger.debug("editing an entry....................")    
    entry = Entry.objects.get(pk=int(entry_id))
    originaltags = entry.tags
    if request.method == "GET":
        form = PublishForm(instance=entry,initial={'tags':' '.join(entry.tags.values_list('name',flat=True))},user=request.user,editmode=entry.id)      
        backto =  request.GET['backto']        
        return render_to_response('publish/institute_create_new.html',{'form':form,'editmode':True,'backto':backto},RequestContext(request))
    elif request.method == "POST":
        form = PublishForm(request.POST, instance=entry,user=request.user)
        if form.is_valid() :
            newentry = form.save(commit=False)            
            newentry.save()
            removeUserTagWeights(originaltags,request.user,settings.CONTRIBUTION_WEIGHT)
            newentry.tags = form.cleaned_data['tags']
            assignUserTagWeights(newentry.tags,request.user,settings.CONTRIBUTION_WEIGHT)            
            if request.POST['whichbutton'] == "save":
                create_message(request,"saved your news letter")
                return HttpResponseRedirect(reverse('editentryurl',kwargs={'entry_id':entry.id})+"?backto="+request.POST['backto'])
            else :            
                if request.POST['backto'] == "publishhome" :
                    create_message(request,"Successfully created blog post")
                    return HttpResponseRedirect(reverse('newsletterurl'))                
                elif request.POST['backto'] == "archive":
                    create_message(request,"Successfully edited the blog post")
                    return HttpResponseRedirect(reverse('archiveurl'))
                else :
                    create_message(request,"Successfully edited the blog post")
                    return HttpResponseRedirect(reverse('mypostsurl'))
        else:
            return render_to_response('publish/institute_create_new.html',{'form':form,'editmode':True,'backto':request.POST['backto']},RequestContext(request))            
                    
                
                
       
    
        

def displaySinglePost(request,entry_id):
    mlogger.debug("display single post with comments")
    entry = Entry.objects.get(pk=entry_id)
    if request.user.is_authenticated() and entry.user.id != request.user.id :
        assignUserTagWeights(entry.tags,request.user,settings.VIEW_WEIGHT)
    return render_to_response('publish/institute_single_post.html',{'entry':entry},RequestContext(request))
    
   
def postComment(request,entry_id):    
    mlogger.debug("post comment url...................")
    d = {}
       
    try:
            if request.method == "POST" :
                c = Comment()
                c.entry = Entry.objects.get(pk=int(entry_id))
                
                if 'username' in request.POST.keys() :                   
                   c.nouser = True
                   c.username = request.POST['username']
                   if len(request.POST['webaddress'].strip()) > 0 :
                        c.webaddress = request.POST['webaddress']               
                else:
                    user = request.user
                    c.user = request.user
                c.text = request.POST['text']                
                c.save()                                                     
                    
                ntext = c.getNText()                            
                
                if len(ntext) == 0 :
                    d['error'] = "Some problem with the comment"
                else:
                    if c.nouser is False:
                        d['text'] = "%s--<a href=\"%s\"> %s </a>"%(c.getNText(),user.get_profile().get_absolute_url(),user.get_profile().fullname)                  
                        d['name'] = user.get_profile().fullname
                    else:
                        if c.webaddress is None :
                                d['text'] = "%s--<a href='#'> %s </a>"%(c.getNText(),c.username)
                        else :
                                d['text'] = "%s--<a href=\"%s\"> %s </a>"%(c.getNText(),c.webaddress,c.username)                        
                        d['name'] = c.username
                        
    except:
        d['error'] = "oops........some problem at the server end"
    
    json = simplejson.dumps(d)
    return HttpResponse(json)
    

@login_required(redirect_field_name='next') 
def getMyPosts(request):
    mlogger.debug("get the post which are posted by user")
    entries = Entry.objects.filter(institute__id=request.institute.id,user__id=request.user.id).order_by('-createddate')
    page = getPage(request)
    return object_list(request, queryset=entries,
                           extra_context={},template_object_name="entry",paginate_by=settings.ARCHIVES_PER_PAGE,page=page,template_name="publish/institute_myposts.html")
 
     

@login_required(redirect_field_name='next')    
def deleteEntry(request,entry_id):
    mlogger.debug("deleting an entry.............")    
    entry = Entry.objects.get(pk=entry_id)
    removeUserTagWeights(entry.tags,request.user,settings.CONTRIBUTION_WEIGHT)
    entry.delete()
    create_message(request,"Successfully deleted the entry")
    return HttpResponseRedirect(reverse('mypostsurl'))
    
@login_required(redirect_field_name='next')  
def deletePaper(request,entry_id):
    mlogger.debug("deleting an entry.............")    
    entry = Entry.objects.get(pk=entry_id)
    removeUserTagWeights(entry.tags,request.user,settings.CONTRIBUTION_WEIGHT)
    entry.delete()
    create_message(request,"Successfully deleted the paper")
    return HttpResponseRedirect(reverse('facultyarchiveurl',kwargs={'faculty_name':entry.user.get_profile().getSlugifyName()}))                
    
    
    

def displayFacultyResearch(request,faculty_name):
    mlogger.debug("displaying the faculty research ")
    faculty_name = faculty_name.replace("-"," ")
    profile = UserProfile.objects.get(fullname__iexact=faculty_name)
    user = profile.user    
    entries = Entry.objects.filter(institute__id=request.institute.id,user__id=user.id,research_paper=True).order_by('-createddate')
    page = getPage(request)    
    return object_list(request, queryset=entries,
                           extra_context={'faculty':user},template_object_name="entry",paginate_by=settings.ENTRIES_PER_PAGE,page=page,template_name="publish/faculty_publish_home.html")
    
    
    

@login_required(redirect_field_name='next')  
def publishNewResearch(request,entry_id=None):
    mlogger.debug("publish new Research")
    if request.method == "GET" :        
        if entry_id is None :
               form = PublishForm(user=request.user)
        else :
               entry=Entry.objects.get(pk=entry_id)
               form = PublishForm(instance=entry,user=request.user)
        return render_to_response('publish/faculty_create_new.html',{'form':form},RequestContext(request))
    elif request.method == "POST" :        
        form = PublishForm(request.POST,user=request.user)
        if form.is_valid() :
            entry = form.save(commit=False)
            entry.institute = request.institute
            entry.user = request.user
            entry.research_paper = True
            entry.save()
            if request.POST['whichbutton'] == "save" :                
                create_message(request,"saved your paper")
                return HttpResponseRedirect(reverse('researchnewurl2',kwargs={'entry_id':entry.id})+"?backto=publishhome")
            else:
                create_message(request,"Successfully created new research paper")
                entry.tags = form.cleaned_data['tags']
                assignUserTagWeights(entry.tags,request.user,settings.CONTRIBUTION_WEIGHT)
                if entry.sendemail is not None :                    
                    emaillist = entry.sendemail.getEmailList(request.institute)
                    fullurl = entry.getfullurl(request.institute)
                    deliverEmail('new_faculty_paper_subject.html','new_faculty_paper.html',{'institute':request.institute,'entry':entry,'fullurl':fullurl},emaillist)
                return HttpResponseRedirect(reverse('facultyresearchurl',kwargs={'faculty_name':entry.user.get_profile().getSlugifyName()}))               
        else:
            return render_to_response('publish/faculty_create_new.html',{'form':form},RequestContext(request))
            
            
            
            
@login_required(redirect_field_name='next')            
def editPaper(request,entry_id):
    mlogger.debug("Edit research paper........................")
    entry = Entry.objects.get(pk=int(entry_id))
    originaltags = entry.tags
    if request.method == "GET":
        form = PublishForm(instance=entry,initial={'tags':' '.join(entry.tags.values_list('name',flat=True))},user=request.user,editmode=entry.id)      
        backto =  request.GET['backto']        
        return render_to_response('publish/institute_create_new.html',{'form':form,'editmode':True,'backto':backto},RequestContext(request))
    elif request.method == "POST":
        form = PublishForm(request.POST, instance=entry,user=request.user)
        if form.is_valid() :            
            form.save()
            newentry = form.save(commit=False)            
            newentry.save()
            removeUserTagWeights(originaltags,request.user,settings.CONTRIBUTION_WEIGHT)
            newentry.tags = form.cleaned_data['tags']
            assignUserTagWeights(newentry.tags,request.user,settings.CONTRIBUTION_WEIGHT)  
            
            if request.POST['whichbutton'] == "save":
                create_message(request,"saved your research paper")
                return HttpResponseRedirect(reverse('editpaperurl',kwargs={'entry_id':entry.id})+"?backto="+request.POST['backto'])
            else :            
                if request.POST['backto'] == "publishhome" :
                    create_message(request,"Successfully created new research paper")
                    return HttpResponseRedirect(reverse('facultyresearchurl',kwargs={'faculty_name':entry.user.get_profile().getSlugifyName()}))                
                elif request.POST['backto'] == "archive":
                    create_message(request,"Successfully edited the paper")
                    return HttpResponseRedirect(reverse('facultyarchiveurl',kwargs={'faculty_name':entry.user.get_profile().getSlugifyName()}))
        else :
            return render_to_response('publish/institute_create_new.html',{'form':form,'editmode':True,'backto':request.POST['backto']},RequestContext(request))
                    
           
                
                
    

def displaySinglePaper(request,entry_id):
    mlogger.debug("display single post with comments")
    entry = Entry.objects.get(pk=entry_id)
    if request.user.is_authenticated() and entry.user.id != request.user.id :
        assignUserTagWeights(entry.tags,request.user,settings.VIEW_WEIGHT)
    return render_to_response('publish/faculty_single_post.html',{'entry':entry},RequestContext(request))
        
        
def displayResearchArchive(request,faculty_name):
    mlogger.debug("display research archives..................")    
    faculty_name = faculty_name.replace("-"," ")
    profile = UserProfile.objects.get(fullname__iexact=faculty_name)
    user = profile.user
    entries = Entry.objects.filter(institute__id=request.institute.id,user__id=user.id,research_paper=True).order_by('-createddate')
    page = getPage(request)    
    return object_list(request, queryset=entries,
                           extra_context={},template_object_name="entry",paginate_by=settings.ARCHIVES_PER_PAGE,page=page,template_name="publish/faculty_publish_archives.html")
    
    

def displayArchives(request):
    mlogger.debug("display archives..................")   
    entries = Entry.objects.filter(institute__id=request.institute.id,research_paper=False).order_by('-createddate')
    page = getPage(request)    
    return object_list(request, queryset=entries,
                           extra_context={},template_object_name="entry",paginate_by=settings.ARCHIVES_PER_PAGE,page=page,template_name="publish/institute_publish_archives.html")
    
    
    
    
    
    
    
    
    
