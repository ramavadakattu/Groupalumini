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

from tagging.models import Tag
from askalumini.views import removeUserTagWeights , assignUserTagWeights
from institution.models import StudentInstitute , FacultyInstitute ,Student , Faculty, UserProfile
from interesting.models import UserTagWeight
from connections.models import Connection

from events.models import Event , EventAttendance
from jobs.models import Job
from askalumini.models import Question , Answer
from payments.models import Donation , Fund
from publish.models import Entry , Comment

from tagging.models import Tag


import datetime
import logging
import logging.config

import re


mlogger = logging.getLogger(__name__)



@login_required(redirect_field_name='next')
def displayHome(request):
    mlogger.debug("Display interesting home......................")
    (friends,ffriends) = recommendFriends(request.user,request.institute,5)
    empty = False
    if not friends :
       if not  ffriends :
           empty = True
           
    return render_to_response("interesting/ihome.html",{'empty':empty,'friends':friends,'ffriends':ffriends,'itag1':'people'},RequestContext(request))
    
@login_required(redirect_field_name='next')    
def getInterestingPeople(request):
    mlogger.debug("Display interesting people......................")
    (friends,ffriends) = recommendFriends(request.user,request.institute,5)
    
    empty = False
    if not friends :
       if not  ffriends :
           empty = True
               
    return render_to_response("interesting/ihome.html",{'friends':friends,'empty':empty,'ffriends':ffriends,'itag1':'people'},RequestContext(request))
    
    
def submitTags(request):
    mlogger.debug("Save the tags for this user")
    d = {}    
    tags = request.POST['tags'].strip()    
    #make sure that the tags are of valid string
    e = re.compile(r"[0-9A-Za-z-. ]+",re.IGNORECASE)
    result = e.match(tags)    
    if result is not None  and len(tags) == result.span()[1] :      
        profile = request.user.get_profile()
        removeUserTagWeights(profile.tags,request.user,settings.PROFILE_WEIGHT)
        profile.tags = tags
        assignUserTagWeights(profile.tags,request.user,settings.PROFILE_WEIGHT)
        #send response
    else:
        d['error'] = "Error:Tags should only contain alphanumeric characters, space,hypen('-'),dot('.'). Tags shoud be saperated by space"
             
    json = simplejson.dumps(d)
    return HttpResponse(json)
    
    
    
def tagLookup(request):
    mlogger.debug("Tag lookup....................")   
    results = []   
    if request.method == "GET":
        if 'q' in request.GET.keys():
            value = request.GET['q'].strip()
            endtag = value.split()[-1]
            
            if len(value) > 0:
                model_results = Tag.objects.filter(name__istartswith=endtag)
                results = [ x.name for x in model_results ]
    json = simplejson.dumps(results)   
    return HttpResponse(json, mimetype='application/json')
    
    
    
def recommendFriends(user,institute,total):
    '''recommedFriends basically recommends other top 5 people who are of similar interests
       
       Pruning Rules :
       ----------------
       if the alumini does belong  to same industry then they will not be treated as friends
       
       Scoring Rules :
       ----------------
       same market (5) more score
       program(1),department(3),course(5),batch(2) scores
       country(1),state(2),city(3) wise scores
       
       Top X tags of one person should belongs to Top Y tags of other person.(number of top X tags matches with Top Y tags)
       
       return a list of top 5 recommended friends
    '''
    profile = user.get_profile()
    
    #no recommended friends from faculty and admin
    if  profile.isadmin :        
        return ([],[])
    elif profile.isStudent :        
            student = profile.student_set.all()[0]            
            friends = getStudentTopFriends(student,institute,total)              
            #student faculty friends
            facultyfriends = getStudentFTopFriends(student,institute,1)
    elif profile.isFaculty :
            onethird = total/3
            remaining = (total - onethird)
            faculty = profile.faculty_set.all()[0]
            #Faculty student friends
            friends = getFacultySFriends(faculty,institute,remaining)
            #Faculty Faculy Friends
            facultyfriends = getFacultyFFriends(faculty,institute,onethird)        
    
    return (friends,facultyfriends)
    
    

def getFacultySFriends(faculty,institute,total):
    ''' getting Faculty Student Friends '''
    fi = FacultyInstitute.objects.get(faculty__id=faculty.id,institute__id=institute.id)
    connections = getUserConnections(faculty.profile.user) 
    students = Student.objects.filter(institutes__in=[institute.id]).exclude(profile__id__in=connections)
    scores = []
    
    for s in students :
           score = 0
           si = StudentInstitute.objects.get(student__id=s.id,institute__id=institute.id)
           
           if si.department.id == fi.department.id :
                score = score + 4
                
           score = score + getScoreFromTags(faculty,s)
           
           scores.append((0,score))
           
    scores.sort(lambda x, y: cmp(x[1],y[1]),reverse=True)        
           
    friends = []   
    #pick the top 5 friends
    for score in scores[:total]:
       #Total best score is 36
       #If user crosses atleast a score of 18 we will show him as a recommended friends      
       if score[1] >= 6 : 
          friends.append(students[score[0]])       
    
    return friends





def getFacultyFFriends(faculty,institute,total):
    ''' getting Faculty Faculty Friends '''
    fi = FacultyInstitute.objects.get(faculty__id=faculty.id,institute__id=institute.id)
    connections = getUserConnections(faculty.profile.user) 
    faculties = Faculty.objects.filter(institutes__in=[institute.id]).exclude(id=faculty.id).exclude(profile__id__in=connections)
    scores = []
    
    for f in faculties :
        score = 0        
        ifi = FacultyInstitute.objects.get(faculty__id=f.id,institute__id=institute.id)
        
        if fi.department.id == ifi.department.id :
            score = score + 4
        
        score = score + getScoreFromTags(faculty,f)
        scores.append((0,score))
        
        
    ffriends = []   
    #pick the top 5 friends
    for score in scores[:total]:
       #Total best score is 36
       #If user crosses atleast a score of 18 we will show him as a recommended friends      
       if score[1] >= 6 : 
          ffriends.append(faculties[score[0]])       
    
    return ffriends    
        
 


def getStudentFTopFriends(student,institute,total):
    ''' getting student Faculty Friends '''
    si = StudentInstitute.objects.get(student__id=student.id,institute__id=institute.id)
    connections = getUserConnections(student.profile.user)
    faculty = Faculty.objects.filter(institutes__in=[institute.id]).exclude(profile__id__in=connections)
    
    scores = []
    
    for f in faculty :
        score = 0
        
        fi = FacultyInstitute.objects.get(faculty__id=f.id,institute__id=institute.id)
        
        if fi.department.id == si.department.id :
            score = score + 4
            
        score = score + getScoreFromTags(student,f)
        #(faculty object position ,score )
        scores.append((0,score))
        
    scores.sort(lambda x, y: cmp(x[1],y[1]),reverse=True)    
    
    ffriends = []   
    #pick the top 5 friends
    for score in scores[:total]:
       #Total best score is 36
       #If user crosses atleast a score of 18 we will show him as a recommended friends      
       if score[1] >= 6 : 
          ffriends.append(faculty[score[0]])       
    
    return ffriends
    
    

def getStudentTopFriends(student,institute,total):
    ''' getting student student friends '''
    #intialize score
    si = StudentInstitute.objects.get(student__id=student.id,institute__id=institute.id)
    #get User Connections
    connections = getUserConnections(student.profile.user)
    profile = student.profile
    #remove already existing connections
    students = Student.objects.filter(institutes__in=[institute.id]).exclude(id=student.id).exclude(profile__id__in=connections)    
    scores = []
    
    for s in students :
        score = 0
        
        if s.industry.id == student.industry.id :
            score = score + 3
        
        if s.market.id  == student.market.id :
            score = score + 5

        #location based scores ...........................
        if s.profile.country.id == profile.country.id :
            score = score + 1
            
            if s.profile.state == profile.state :
                score = score +2                
                
                if s.profile.city == profile.city :
                    score = score +5
                
        isi = StudentInstitute.objects.get(student__id=s.id,institute__id=institute.id)     
        
        #passout year score
        #more nearer the passout the more score that this connection will get
        if si.toyear > isi.toyear :
            x=si.toyear
            y=isi.toyear
        elif isi.toyear >=  si.toyear :
            x = isi.toyear
            y = si.toyear
        
        
        if x-y == 0 :
            score = score + 4
        elif x-y <= 2 :    
            score = score + 2
        elif x-y <=5 :
            score = score + 1
         
        
        #degree department and course matching.................
        if si.degree.id == isi.degree.id :
            score = score +1
        
        if si.department.id == isi.department.id :
            score = score +2
            
        if si.course.id == isi.course.id :
            score = score +5
            
        score = score + getScoreFromTags(student,s)
        #This score belongs to 0 position student object...............
        scores.append((0,score))
        
    #sort the scores list
    scores.sort(lambda x, y: cmp(x[1],y[1]),reverse=True)
       
    friends = []   
    #pick the top 5 friends
    for score in scores[:total]:
       #Total best score is 36
       #If user crosses atleast a score of 18 we will show him as a recommended friends      
       if score[1] > 18 : 
          friends.append(students[score[0]])       
    
    return friends    
        
        
        
def getUserConnections(user):
    ''' get all the user connections as a list '''    
    profile = user.get_profile()
    connections = []
    con1 = list(Connection.objects.filter(initiator__id=profile.id,pending=False).values_list('reciever__id',flat=True))
    con2 = list(Connection.objects.filter(reciever__id=profile.id,pending=False).values_list('initiator__id',flat=True))
    connections = con1 + con2    
    mlogger.debug("His connections = %s"%(str(connections)))
    return connections
    
        
def getScoreFromTags(student,s):
    '''  As of now lets us just take a note of 5 top density tags '''
    studentuser = student.profile.user
    suser = s.profile.user
    
    #get all the tags of studentuser ordered by weight
    topusertags = UserTagWeight.objects.values_list('tag__name',flat=True).filter(user__id=studentuser.id).order_by('-weight')
    topusertags = list(topusertags)[:5]
    
    
    #get all the tags of s ordered by weight
    topstags =  list(UserTagWeight.objects.values_list('tag__name',flat=True).filter(user__id=suser.id).order_by('-weight'))
    
    score = 0
    for tag in topusertags :
        index1 = topusertags.index(tag)
        if tag in topstags :
            index2 = topstags.index(tag)
            
            if index2 <= index1 :
                score = score +1
            else :
                score = score + (index1/float(index2))                
    
    #scale the score to the level of 8
    if score >= 5 :
        score = score + 3
    elif score < 5  and score >=  4 :
        score = score + 2
    elif score < 4  and score >=  3 :
        score = score + 1
    else :
        score = score + 0.5
                    
    return score        
          

def getInterestingContent(request):
    tags =  getTopUserTags(request.user,5)   
    questions = Question.tagged.with_any(tags,queryset=Question.objects.filter(institute__id=request.institute.id))[:10]
    return render_to_response("interesting/ihome.html",{'questions':questions,'itag1':'content','itag2':'questions'},RequestContext(request))

            
            
def getInterestingJobs(request):
    tags =  getTopUserTags(request.user,5)   
    jobs = Job.tagged.with_any(tags,queryset=Job.objects.filter(institute__id=request.institute.id))[:10]
    return render_to_response("interesting/ihome.html",{'jobs':jobs,'itag1':'content','itag2':'jobs'},RequestContext(request))


def getInterestingEvents(request):
    tags =  getTopUserTags(request.user,5)    
    events = Event.tagged.with_any(tags,queryset=Event.objects.filter(institute__id=request.institute.id))[:10]
    return render_to_response("interesting/ihome.html",{'events':events,'itag1':'content','itag2':'events'},RequestContext(request))


def getInterestingDiscussions(request):
    tags =  getTopUserTags(request.user,5)    
    questions = Question.tagged.with_any(tags,queryset=Question.objects.filter(institute__id=request.institute.id))[:10]
    return render_to_response("interesting/ihome.html",{'questions':questions,'itag1':'content','itag2':'questions'},RequestContext(request))



def getTopUserTags(user,total):
    topusertags = UserTagWeight.objects.values_list('tag__id',flat=True).filter(user__id=user.id).order_by('-weight')
    topusertags = list(topusertags)[:total]
    mlogger.debug("Top user tags = %s " %(str(topusertags)))
    tags = []
    for tag in topusertags :
        tags.append(Tag.objects.get(pk=tag).name)
    return tags


def getInterestingResearchPapers(request):
    tags =  getTopUserTags(request.user,5)    
    papers = Entry.tagged.with_any(tags,queryset=Entry.objects.filter(institute__id=request.institute.id,research_paper=True))[:10]
    return render_to_response("interesting/ihome.html",{'papers':papers,'itag1':'content','itag2':'papers'},RequestContext(request))

    


    
    
    
    
        
        
            
            

    
         
    
    
    
    
    


