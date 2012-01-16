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
from institution.models import deliverEmail , Student , StudentInstitute ,Department ,Course
 
from profile.views import getPage

import datetime
import logging
import logging.config

from institution.models import UserProfile
from statistics.models import Industry,Market
from django.db.models import  Count , Min

mlogger = logging.getLogger(__name__)# Create your views here.




def displayStatHome(request):
    mlogger.debug("Stats ............... Home........................")
    industrystats = Student.objects.filter(institutes__in=[request.institute.id],industry__isnull=False).values('industry__name','industry__id').annotate(Count('id'))
    departmentstats = StudentInstitute.objects.filter(institute__id=request.institute.id).values('department__name','department__id').annotate(Count('id'))
    batchstats = getBatchWiseStats(request.institute,sort=True)        
    return render_to_response('statistics/stat_home.html',{'industrystats':industrystats,'departmentstats':departmentstats,'batchstats':batchstats},RequestContext(request))    
    
    
def showIndustryStats(request):
    mlogger.debug("Industry stats ...................................")
    #Calculate People by industry      
    industrystats = Student.objects.filter(institutes__in=[request.institute.id],industry__isnull=False).values('industry__name','industry__id').annotate(industry_count=Count('id')).order_by('-industry_count')   
    return render_to_response('statistics/industry_stats.html',{'industrystats':industrystats},RequestContext(request))

def showIndustryMarketStats(request,industryid):
    mlogger.debug("Markets ..................")
    industryid = int(industryid)
    industry = Industry.objects.get(pk=industryid)
    #Now get the market wise statistics    
    marketstats = Student.objects.filter(industry__id=industry.id,industry__isnull=False,market__isnull=False).values('industry__name','market__name').annotate(market_count=Count('id')).order_by('-market_count')     
    return render_to_response('statistics/industry_market_stats.html',{'industry':industry,'marketstats':marketstats},RequestContext(request))
    
    
def showDepartmentStats(request):
    mlogger.debug("Department stats ...............................")
    departmentstats = StudentInstitute.objects.filter(institute__id=request.institute.id).values('department__name','department__id').annotate(department_count=Count('id')).order_by('-department_count') 
    return render_to_response('statistics/department_stats.html',{'departmentstats':departmentstats},RequestContext(request))
    
    
    
def showDepartmentCourseStats(request,department_id):
    mlogger.debug("Department Course stats ...............................")
    department_id=int(department_id)
    department = Department.objects.get(pk=department_id)
    coursestats = StudentInstitute.objects.filter(institute__id=request.institute.id,department__id=department_id).values('department__name','course__name','course__id').annotate(course_count=Count('id')).order_by('-course_count') 
    return render_to_response('statistics/department_course_stats.html',{'department':department,'coursestats':coursestats},RequestContext(request))
    
    
def showBatchWiseStats(request):
    mlogger.debug("Showing batch wise stats ..............................")
    batchstats = getBatchWiseStats(request.institute)
    sortedbatchstats = list(batchstats)
    sortedbatchstats.sort(lambda x, y: cmp(x[1],y[1]),reverse=True)
    return render_to_response('statistics/batchwise_stats.html',{'batchstats':batchstats,'sortedbatchstats':sortedbatchstats},RequestContext(request))
    
    
def getBatchWiseStats(institute,sort=False):
    #Find the 
    minyear = StudentInstitute.objects.filter(institute__id=institute.id).aggregate(Min('fromyear'))['fromyear__min']    
    thisyear = datetime.datetime.today().year
    
    bucketsize = settings.BATCH_BUCKET_SIZE
    
    if minyear is not None: 
       remainder =  minyear % bucketsize
    else :
       remainder = 0
       minyear = 1950
        
    if remainder == 0 :
        baseyear =  (minyear + remainder) - bucketsize
    else :
        baseyear =  minyear
    
    yearstart = baseyear
    batchstats =[]
    
    while yearstart <= thisyear :
        if yearstart == baseyear :
             yearend = yearstart + bucketsize
        else :
             yearend = yearstart + bucketsize -1
        mlogger.debug("Bucket from %d -- %d "%(yearstart,yearend))
        #Find all the students who fall into this slot
        count = StudentInstitute.objects.filter(institute__id=institute.id,fromyear__gte=yearstart,toyear__lte=yearend).count()
        bucketstring = "%s-%s"%(str(yearstart),str(yearend))
        batchstats.append((bucketstring,count))
        yearstart = yearend + 1
    
    if sort :
        #sort the batchstats based on count
        batchstats.sort(lambda x, y: cmp(x[1],y[1]),reverse=True)
    
    return batchstats     
    



@login_required(redirect_field_name='next')      
def showDegreeStats(request,department_id,course_id) :
    mlogger.debug("Department Course  Degree stats ...............................")
    department_id=int(department_id)
    department = Department.objects.get(pk=department_id)
    course_id =int(course_id)
    course = Course.objects.get(pk=course_id)    
    degreestats = StudentInstitute.objects.filter(institute__id=request.institute.id,department__id=department_id,course__id=course_id).values('department__name','course__name','degree__name').annotate(degree_count=Count('id')).order_by('-degree_count')     
    return render_to_response('statistics/degree_stats.html',{'course':course,'department':department,'degreestats':degreestats},RequestContext(request))
    
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    



    
    
    




