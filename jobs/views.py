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

from institution.models import deliverEmail
from askalumini.views import removeUserTagWeights , assignUserTagWeights

import feedparser

import datetime
import logging
import logging.config


from jobs.models import Job,JobComment
from jobs.forms import JobForm
from askalumini.forms import QuestionForm,AnswerForm
from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , photo_file_path
from profile.models import ShortMessages
from django.views.generic.list_detail import object_list

from profile.views import getPage


mlogger = logging.getLogger(__name__)
# Create your views here.




@login_required(redirect_field_name='next') 
def displayJobs(request):
    mlogger.debug("diplaying paginated list of jobs")
    page = getPage(request)
    jobs = Job.objects.filter(   Q(institute__isnull=True) | Q(institute__id=request.institute.id)  ).order_by('-createddate')
  
    
    return object_list(request, queryset=jobs,
                           extra_context={},template_object_name="job",paginate_by=settings.JOBS_PER_PAGE,page=page,template_name="jobs/display_jobs.html")

@login_required(redirect_field_name='next') 
def postAJob(request):
    mlogger.debug("posting a job.......................")    
    if request.method == "GET":
        form  = JobForm(user=request.user)        
        return render_to_response('jobs/postjob.html',{'form':form},RequestContext(request))
    elif request.method =="POST":
        form =  JobForm(request.POST,user=request.user)
        if form.is_valid() :
            j=form.save(commit=False)                        
            j.postedby = request.user
            j.institute = request.institute
            j.save()
            
            if j.sendemail is not None :
                emaillist = j.sendemail.getEmailList(request.institute)
                fullurl = j.getfullurl(request.institute)
                deliverEmail('new_job_subject.html','new_job_message.html',{'institute':request.institute,'job':j,'fullurl':fullurl},emaillist)
                
            #Assign tags to jobs    
            j.tags = form.cleaned_data['tags']
            assignUserTagWeights(j.tags,request.user,settings.CONTRIBUTION_WEIGHT)          
            create_message(request,"Successfuly posted your job")
            return HttpResponseRedirect(reverse('displayjoburl'))            
        else:
           return render_to_response('jobs/postjob.html',{'form':form},RequestContext(request))
           
           
@login_required(redirect_field_name='next')            
def fetchEntityDetail(user,institute):    
    profile = user.get_profile()
    if profile.isStudent :
        s = Student.objects.get(profile__id = profile.id )
        si = StudentInstitute.objects.get(student__id = s.id,institute__id=institute.id)
        return si
    else:        
        f = Faculty.objects.get(profile__id = profile.id )
        fi = FacultyInstitute.objects.get(faculty__id = f.id,institute__id=institute.id)
        return fi
    
    

@login_required(redirect_field_name='next') 
def viewJob(request,jobid):
    ''' view the above jobid '''
    j = Job.objects.get(pk=int(jobid))
    if j.postedby is not None :
        if request.user.id != j.postedby.id  :
            assignUserTagWeights(j.tags,request.user,settings.VIEW_WEIGHT)                            
    return render_to_response('jobs/viewjob.html',{'job':j},RequestContext(request))
    
@login_required(redirect_field_name='next')     
def deleteJob(request,jobid):
    ''' delete the above jobid '''
    j = Job.objects.get(pk=int(jobid))
    removeUserTagWeights(j.tags,request.user,settings.CONTRIBUTION_WEIGHT)
    j.delete()
    create_message(request,"Successfuly deleted the job")
    return HttpResponseRedirect(reverse('displayjoburl'))       
    
    
@login_required(redirect_field_name='next')    
def postJobComment(request,jobid):  
    d = {}    
    try:
            if request.method == "POST" :        
                user = request.user                
                jc = JobComment()
                jc.job = Job.objects.get(pk=int(jobid))
                jc.postedby = request.user
                jc.text = request.POST['text']
                jc.save()                             
                
                ntext = jc.getNText()                            
                
                if len(ntext) == 0 :
                    d['error'] = "Some problem with the comment"
                else:
                    d['text'] = "%s--<a href=\"%s\"> %s </a>"%(jc.getNText(ajax=True),user.get_profile().get_absolute_url(),user.get_profile().fullname)                  
                    d['name'] = user.get_profile().fullname
    except:
        d['error'] = "oops........some problem at the server end"
    
    json = simplejson.dumps(d)
    return HttpResponse(json)
    
    
@login_required(redirect_field_name='next')        
def editJob(request,jobid):
    jobid = int(jobid)
    job = Job.objects.get(pk=jobid)
    originaltags = job.tags
    if request.user.id == job.postedby.id :
        if request.method == "GET" :
            mlogger.debug("the person who posted the job is editing")
            form = JobForm(instance=job,initial={'tags':' '.join(job.tags.values_list('name',flat=True))},user=request.user)            
            return render_to_response('jobs/postjob.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
            form = JobForm(request.POST, instance=job,user=request.user)
            if form.is_valid() :
                newjob = form.save(commit=False)
                newjob.save()
                removeUserTagWeights(originaltags,request.user,settings.CONTRIBUTION_WEIGHT)                
                newjob.tags = form.cleaned_data['tags']
                #what about tags brother                  
                assignUserTagWeights(newjob.tags,request.user,settings.CONTRIBUTION_WEIGHT)                            
                create_message(request,"Successfuly edited your job")
                return HttpResponseRedirect(reverse('displayjoburl'))
            else:
                return render_to_response('jobs/postjob.html',{'form':form,'editmode':True},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this job")
        return HttpResponseRedirect(reverse('viewjoburl',kwargs={'jobid':job.id}))
        
        
     
    
        
        
    
 