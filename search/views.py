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
import re


from askalumini.models import Question,Answer,Comment
from askalumini.forms import QuestionForm,AnswerForm
from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , photo_file_path
from profile.models import ShortMessages
from django.views.generic.list_detail import object_list

from whoosh.qparser import QueryParser
from whoosh import index


mlogger = logging.getLogger(__name__)


def alumClubSearch(request,pageno=1) :
     institute = request.institute
     instituteid = unicode(institute.id)
    
     if request.method ==  "GET" :         
          if 'query' in request.GET.keys() :
               mlogger.debug("searching for given search string...........%s " %(request.method,))
               query = request.GET['query']            
               ix = index.open_dir(settings.WHOOSH_INDEX) 
               parser = QueryParser("content",schema= ix.schema)
               pstring = query+"  "+" AND instituteid :"+instituteid
               mlogger.debug("parse string  %s" % pstring)
               query = parser.parse(pstring)
               searcher = ix.searcher()
               ix.close()
               nofetch = int(pageno) *  settings.SEARCH_PAGE_SIZE
               hitlist = searcher.search(query,limit=nofetch)               
               newhitlist = getAppropriateSubset(hitlist,pageno)               
               
               entitylist = getEntities(newhitlist)               
               hits = zip(newhitlist,entitylist)
               size_of_page = settings.SEARCH_PAGE_SIZE
               current_page_length = len(hits)
               
               #Pagination logic
               pageno = int(pageno)
               
               next_page = False               
               next_page_no = pageno + 1
               
               prev_page = False
               prev_page_no = pageno - 1
              
          
               if current_page_length == size_of_page :
                    next_page = True
                    
               if pageno > 1 :
                    prev_page = True
               
               mlogger.debug("how many hits %s"%str(len(hits)) )              
               return render_to_response("search/search.html",{'hits':hits,
                                                               'query':request.GET['query'],
                                                               'next_page':next_page,
                                                               'next_page_no':next_page_no,
                                                                'prev_page':prev_page,
                                                                'prev_page_no':prev_page_no},RequestContext(request))          
          else:
               return render_to_response("search/search.html",{},RequestContext(request))    
               
          
           


def getAppropriateSubset(hitlist,pageno):
     '''  pagination with whoosh index'''
     pageno = int(pageno)
     if pageno == 1 :
          return hitlist
     else:
        if hitlist.scored_length() >  (pageno-1) * settings.SEARCH_PAGE_SIZE :
           starting_index =  ((pageno-1) * settings.SEARCH_PAGE_SIZE )
           ending_index = hitlist.scored_length()
           return hitlist[starting_index:ending_index]
        else :
          return []
  
           
            
def getEntities(hitlist):    
    entitylist = []
    for h in hitlist :
        id = h['id']
        p = re.compile("\d+[a-zA-Z]+(?P<entityid>\d+)")
        entityid = int(p.search(id).group('entityid'))
        
        if id.find("student") >= 0:
            student = Student.objects.get(pk=entityid)
            entitylist.append(student)
        elif id.find("faculty") >= 0:
            faculty = Faculty.objects.get(pk=entityid)
            entitylist.append(faculty)
    
    return entitylist        
        
        

            
            
            
            
            
            
            
            
        
     
