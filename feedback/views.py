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

import datetime
import logging
import logging.config

from institution.models import deliverEmail
from payments.views import getAlumClubAdminEmail
from location.models import Country,State
from feedback.models import Feedback
import random, sha

mlogger = logging.getLogger(__name__)



def submitFeedback(request):
    d = {}
   

    try:
            if request.method == "POST" :                 
                f = Feedback()
                f.email = request.POST['email']
                f.username = request.POST['name']
                f.message = request.POST['body']
                f.save()
                deliverEmail("feedbacksubject.html","feedbackmessage.html",{'f':f},getAlumClubAdminEmail())
               
    except:
        d['error'] = "oops........some problem at the server end"
    
    json = simplejson.dumps(d)
    return HttpResponse(json)  





