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
from django.http import get_host
from django.utils.html import escape

import datetime
import logging
import logging.config

from institution.models import deliverEmail
from payments.views import getAlumClubAdminEmail
from location.models import Country,State

import random, sha
import atom
import gdata.contacts
import gdata.contacts.service
import cgi

#from yahoo.application import OAuthApplication


#from contactgrabber import grab_contacts

mlogger = logging.getLogger(__name__)
GMAILSERVICE = "gmail"
YAHOOSERVICE = "yahoo"


GOOGLE_END_POINT = "http://www.google.com/m8/feeds/"

def fetchContactsHome(request):
    
    if request.method == "GET":   
        return render_to_response('fetchcontacts/invitehome.html',{},RequestContext(request))        
    elif request.method == "POST" :
        service = request.POST.get('service',None)
        if service.lower() == GMAILSERVICE:
            next = getFullContactsUrl(request.institute)
            scope = GOOGLE_END_POINT
            secure = False
            session = True
            gd_client = gdata.contacts.service.ContactsService()
            authSubLogin = gd_client.GenerateAuthSubURL(next, scope, secure, session)
            return HttpResponseRedirect(authSubLogin)
        elif service == YAHOOSERVICE :
            oauthapp = OAuthApplication(settings.CONSUMER_KEY, settings.CONSUMER_SECRET,settings.APPLICATION_ID, getFullYahooContactsUrl(request.institute))
            # Step 1. Request user oauth.            
            try:
                request_token = oauthapp.get_request_token(getFullYahooContactsUrl(request.institute))
                request.session['yahoo_request_token'] = request_token
                auth_url = oauthapp.get_authorization_url(request_token)    
                return HttpResponseRedirect(auth_url)
            except Exception, e:
                error = _("Something went wrong!")


def fetchYahooContacts(request):
    '''
    fetches the Yahoo contacts by following the approach
    '''
    
    oauthapp = OAuthApplication(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.APPLICATION_ID, getFullYahooContactsUrl(request.institute))
    error = None
    parsed_contacts = []
    # This is retry mechanism to start new contacts retrieval process.
    retry_url = "%s?retry=" % reverse("yahoocontactsurl")
    if "retry" in request.GET:
        del request.session["yahoo_access_token"]
        del request.session["yahoo_request_token"]

    access_token = request.session.get("yahoo_access_token", None)

    if access_token:
        # Step 3. Read contacts.
        oauthapp.token = access_token
        contacts = oauthapp.getContacts(limit="max")

        if contacts and "error" not in contacts:
            for c in contacts["contacts"]["contact"]:
                email = None
                name = None
                for f in c["fields"]:
                    if f["type"] == "email":
                        email = f["value"]
                    if f["type"] == "name":
                        name = " ".join([f["value"]["givenName"], f["value"]["familyName"]])
                if email:
                    parsed_contacts.append({"name": name, "email": email})
        else:
            # In case of error.
            description = ''
            if "error" in contacts:
                description = contacts["error"].get('description', '')
                if description.find('oauth_problem="token_expired"') > -1:
                    # Retry getting contacts if token expired.
                    return http.HttpResponseRedirect(retry_url)

            # Other unexpected error.
            error = _("Something went wrong! Can't load yahoo contacts.")
            if description:
                error = " ".join([error, description])

    elif "oauth_token" in request.GET and "oauth_verifier" in request.GET and 'yahoo_request_token' in request.session:
        # Step 2. Request access token.
        request_token = request.session['yahoo_request_token']
        if request_token.key == urllib.unquote(request.GET.get('oauth_token', 'no-token')):
            access_token = oauthapp.get_access_token(request_token, request.GET["oauth_verifier"])
            request.session["yahoo_access_token"] = access_token

            return http.HttpResponseRedirect(reverse("yahoocontactsurl"))
        else:
            error = _("Something went wrong! Tokens do not match.")
    

def fetchGmailContacts(request):    
    gd_client = gdata.contacts.service.ContactsService()   
    auth_sub_token = gdata.auth.extract_auth_sub_token_from_url(get_full_url(request))    
    gd_client.UpgradeToSessionToken(auth_sub_token)
    #Fetch atleast 1000 contacts
    query = gdata.contacts.service.ContactsQuery()
    query.max_results = 1000    
    feed = gd_client.GetContactsFeed(query.ToUri())
    PrintFeed(feed)

def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(get_host(request))
    return '%s://%s' % (protocol, host)
    
    
    
def get_full_url(request):
    return get_url_host(request) + request.get_full_path()    

def getFullContactsUrl(institute):
        ''' brings entire url with the domain name '''
        url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,reverse('gmailcontactsurl'))
        return url
    
#get full yahoo url
def getFullYahooContactsUrl(institute):
        ''' brings entire url with the domain name '''
        url =  "http://%s%s%s" %(institute.subdomain.strip(),settings.DOMAIN,reverse('yahoocontactsurl'))
        return url

    

# Create your views here.

def PrintFeed(feed):
  for i, entry in enumerate(feed.entry):
    print '\n%s %s' % (i+1, entry.title.text)
    if entry.content:
      print '    %s' % (entry.content.text)
    # Display the primary email address for the contact.
    for email in entry.email:
      if email.primary and email.primary == 'true':
        print '    %s' % (email.address)
    # Show the contact groups that this contact is a member of.
    for group in entry.group_membership_info:
      print '    Member of group: %s' % (group.href)
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlobString()
      print '    Extended Property - %s: %s' % (extended_property.name, value)


