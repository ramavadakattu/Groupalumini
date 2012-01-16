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

from interesting.models import UserTagWeight


mlogger = logging.getLogger(__name__)



def askHome(request):
    ''' dispaly all question '''
    mlogger.debug("ask alumini home.......................")
    page = getPage(request)    
    #display paginated list of question that are asked
    institution = request.institute
    questions = institution.question_set.all().order_by('-createddate')    
    return object_list(request, queryset=questions,
                           extra_context={ },template_object_name="questions",paginate_by=settings.QUESTION_PER_PAGE,page=page,template_name="askalumini/askhome.html")        
   
    
def getPage(request):
    '''returns the page number from this request'''
    page = None
    try :
        page = int(request.GET['page'])        
    except KeyError :
        page = 1
        
    return page  
   
@login_required(redirect_field_name='next')    
def askQuestion(request):
    ''' display form which allows user to ask question'''
    mlogger.debug("Ask question.................")
    if request.method == "GET" :
        form = QuestionForm()
        return render_to_response("askalumini/askquestion.html",{'form':form},RequestContext(request))
    else :        
        form = QuestionForm(request.POST)       
        if form.is_valid() :
            question = form.save(commit=False)
            question.user = request.user
            question.institute = request.institute
            question.save()
            question.tags=form.cleaned_data['tags']           
            assignUserTagWeights(question.tags,request.user,settings.CONTRIBUTION_WEIGHT)            
            create_message(request,"Sucessfully posted your question")
            return HttpResponseRedirect(reverse('askaluminiurl'))
        else :
            pass
            #we will pass the same form
         
        return render_to_response("askalumini/askquestion.html",{'form':form},RequestContext(request))
        


def displayQuestion(request,questionno):
    ''' display question and its answers'''    
    q = Question.objects.get(pk=questionno)
    answers = q.answer_set.all().order_by('createddate')
    page = getPage(request) 
    if request.method == "GET":
        mlogger.debug("Display question and its answers.................")
        form = AnswerForm()
        if request.user.id != q.user.id  :
            assignUserTagWeights(q.tags,request.user,settings.VIEW_WEIGHT)
        return object_list(request, queryset=answers,
                               extra_context={'question':q , 'form':form},template_object_name="answers",paginate_by=settings.ANSWERS_PER_PAGE,page=page,template_name="askalumini/question.html")
    elif request.method == "POST":
        mlogger.debug("REcieve answer")
        form = AnswerForm(request.POST)
        if form.is_valid() :
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = q
            answer.institute = request.institute
            answer.save()
            create_message(request,"Sucessfully posted your answer")
            return HttpResponseRedirect(reverse('displayquestionurl',kwargs={'questionno':q.id}))
        else :
            return object_list(request, queryset=answers,
                               extra_context={'question':q , 'form':form},template_object_name="answers",paginate_by=settings.ANSWERS_PER_PAGE,page=page,template_name="askalumini/question.html")
       
    


def postAnswer(request):
    ''' handle the post answer form'''    
    pass
    
    
@login_required(redirect_field_name='next')     
def postComment(request):
    ''' handle the comments from the user'''
  
        
    if request.method == "POST":       
        entity = request.POST['entity']
        id = int(request.POST['id'])
        text = request.POST['text']
        divbox = request.POST['divbox']
        commentbox = request.POST['commentbox']
        
        d = {}
        
        d['divbox']  = divbox
        d['commentbox'] = commentbox
        d['commentbuttonbox'] = request.POST['commentbuttonbox']
        d['textareabox'] = request.POST['textareabox']
        c = Comment()
        c.text = text
        c.user = request.user
                
        if entity.find("question")  >= 0:
            c.content_object = Question.objects.get(pk=id)
        else :
            c.content_object = Answer.objects.get(pk=id)
            
        c.save()
        d['error'] = "success"
        d['text'] = "<div class='%s'> %s -- %s </div>" % ('commenttextbox',c.getNText(),c.user.get_profile().fullname)
        json = simplejson.dumps(d)         
        return HttpResponse(json)    
        
            
        
        
 
def assignUserTagWeights(tags,user,weight):
    ''' associates the tags to user
        and for each tags we also note down the weight '''    
    utw = UserTagWeight()
    mlogger.debug("assigning User Tag Weight")
    for tag in tags :
        #is the association between user and tag already exists
        try :
            utw = UserTagWeight.objects.get(user__id=user.id,tag__id=tag.id)
        except UserTagWeight.DoesNotExist :
            utw = UserTagWeight()
            utw.user = user
            utw.tag = tag
            utw.weight = 0
            
        utw.weight = utw.weight+weight
        utw.save()
        
        
def removeUserTagWeights(tags,user,weight):
    ''' remove the tags and their corresponding weight associated to user'''
    
    mlogger.debug("Removing User Tag Weight")
    for tag in tags :
        #is the association between user and tag already exists
        try :
            utw = UserTagWeight.objects.get(user__id=user.id,tag__id=tag.id)
            new_weight = utw.weight - weight
            if new_weight <= 0:
                utw.delete()
            else :
                utw.weight = new_weight
                utw.save()                
        except UserTagWeight.DoesNotExist :
            mlogger.debug("user %s tag %s weight should exist is it n't"%(user.get_profile().fullname,tag.name))
            pass        
        

        

def editQuestion(request,questionno):
    ''' editing a question '''   
    questionid = int(questionno)
    question = Question.objects.get(id=questionid)
    originaltags = question.tags
    if request.user.id == question.user.id :
        if request.method == "GET" :
            mlogger.debug("the person who posted the question is editing")           
            form = QuestionForm(instance=question,initial={'tags':' '.join(question.tags.values_list('name',flat=True))})            
            return render_to_response('askalumini/askquestion.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
            form = QuestionForm(request.POST,instance=question)
            if form.is_valid() :
                   newquestion = form.save(commit=False)
                   newquestion.save()
                   removeUserTagWeights(originaltags,request.user,settings.CONTRIBUTION_WEIGHT)
                   newquestion.tags = form.cleaned_data['tags']                  
                   #what about tags brother                  
                   assignUserTagWeights(newquestion.tags,request.user,settings.CONTRIBUTION_WEIGHT)            
                   create_message(request,"Successfuly edited the event")
                   return HttpResponseRedirect(reverse('askaluminiurl')) 
            else:      
                   return render_to_response('askalumini/askquestion.html',{'form':form,'editmode':True},RequestContext(request))  
            
    else :
        create_message(request,"You are not authorized to edit this question")
        return HttpResponseRedirect(reverse('askaluminiurl'))



def deleteQuestion(request,questionno):
    ''' deleting a question '''
    question = Question.objects.get(pk=questionno)
    removeUserTagWeights(question.tags,request.user,settings.CONTRIBUTION_WEIGHT)
    question.delete()
    create_message(request,"Sucessfully deleted the new question")
    return HttpResponseRedirect(reverse('askaluminiurl'))


        
        
        
        
        
        