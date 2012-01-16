from localsettings import *
import logging
import logging.config
import os
import socket

from django.conf import global_settings

# Django settings for alumclub project.

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
serveripaddress = '174.143.207.130'


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rama Vadakattu', 'rama.vadakattu@gmail.com'),
     ('Vivek Kumar','vivek.kumar.sp@gmail.com'),
     ('Rishav Rastogi','rishav.rastogi@gmail.com'),    
)

#Prefix for the email which raised because of error in server 
EMAIL_SUBJECT_PREFIX = "[Django Error]"

#SEND_BROKEN_LINK_EMAILS = True

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'appmedia')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/appmedia/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sx1kjk45%mxh%(q(fhrtpp!fxf=cn#e6@c-c2chsr(x5cf9gcs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'institution.subdomainmiddleware.SubdomainMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)



ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'debug_toolbar',
    'django_extensions',
    'south',
    'template_utils',
    'sorl.thumbnail',
    'session_messages',
    'voting',
    'connections',
    
    #Internal apps
    'institution',
    'askalumini',
    'profile',
    'search',
    'jobs',
    'events',
    'publish',
    'location',
    'tagging',
    'payments',
    'statistics',
    'mailgroups',
    'interesting',
    'feedback'
    
)

#user profile settings
AUTH_PROFILE_MODULE = 'institution.UserProfile'


#authentication backends
AUTHENTICATION_BACKENDS = (
    'institution.emailbackend.EmailBackEnd',
    'django.contrib.auth.backends.ModelBackend',


)

DEFAULT_IMAGE = "images/default.gif"


LOGIN_URL = "/"

SESSION_COOKIE_DOMAIN = '.groupalumni.com'

#Append out new template processors to already existing processors
templist = list(global_settings.TEMPLATE_CONTEXT_PROCESSORS)
templist.append("institution.context_processors.get_institute")
templist.append("session_messages.context_processors.session_messages")
TEMPLATE_CONTEXT_PROCESSORS = tuple(templist)


#initialize logging
#LOG_FILE_PATH in django
#LOG_FILE_PATH = "\""+os.path.join(os.path.dirname(os.path.normpath(__file__)),"logs.txt")+"\""
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)),"logs.txt")

#LOG FILE NAME In django
LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.normpath(__file__)),'logging.conf')
 


logging.config.fileConfig(LOG_FILE_NAME,defaults=dict(log_path=LOG_FILE_PATH))



#FORUM OR ASK ALUMINI settings
QUESTION_PER_PAGE = 5

ANSWERS_PER_PAGE = 5


#PROFILE MESSAGES
PROFILE_MESSAGES = 6


#short message characters
SHORT_MSG_CHARS = 300


#whoosh configurations.............
WHOOSH_INDEX =  os.path.join(SITE_ROOT, 'indexes')


#Google Maps API key
#Change the key of need
#Alumclub .net
#maps_api_key ="ABQIAAAA1-qENYBwsI3vWi4w_b2G8xRMCYAjTszF-pCrQXMZ0rm8NkL1DxT92rri1gFMOamCoD9IC0XuVAsQ2g"



#group alumni.com API key
#maps_api_key ="ABQIAAAA1-qENYBwsI3vWi4w_b2G8xThoykjXNvoZiVZMNLJK1UWwsDB3BSme7MTjx1A85uTyBf0e81srhwU4w"


#local instance
if socket.gethostbyname(socket.gethostname()) == serveripaddress :
      maps_api_key ="ABQIAAAA1-qENYBwsI3vWi4w_b2G8xThoykjXNvoZiVZMNLJK1UWwsDB3BSme7MTjx1A85uTyBf0e81srhwU4w"
else :    
      maps_api_key ="ABQIAAAA1-qENYBwsI3vWi4w_b2G8xQptDmXe38Qxvat03uACRGxbee2qxR0yYS4RxdOJcvQKJAh17ghEEay-Q"
      
      




#Map related enquiries
PEOPLE_PER_PAGE = 20


#domains
DOMAIN_NAME = ".groupalumni.com"



#jobs related settings
JOBS_PER_PAGE = 10


#events related settings
EVENTS_PER_PAGE = 10



#CKFinder settings

# RESOURCE_TYPE_MAP allows you to map FCKeditor's resource types
# (Image, File, etc) to other paths; these are still appended to
# both [FCKEDITOR_CONNECTOR_ROOT|FCKEDITOR_CONNECTOR_URL] + PREFIX

UPLOAD_URL = '/appmedia/uploads/'
UPLOAD_PATH = "%s/uploads/" % (MEDIA_ROOT,)


#Ich tu alles in uploads
RESOURCE_TYPE_MAP = {
    'Image' : 'uploads',
    'File' : 'uploads',
    'Flash' : 'uploads',
    'None' : 'uploads',
}



#NO of BLOG posts
ENTRIES_PER_PAGE = 8


#number of archives poer page
ARCHIVES_PER_PAGE = 30


#Funds per page
FUNDS_PER_PAGE = 40




#paypal end points
PAYPAL_API = "https://api-3t.sandbox.paypal.com/nvp"

#live environment
#https://api-3t.paypal.com/nvp
#sanbox environment
#https://api-3t.sandbox.paypal.com/nvp



#paypal url
#for sandbox
#https://www.sandbox.paypal.com/webscr&cmd=_express-checkout&token=
#for live environment
#https://www.paypal.com/webscr?cmd=_express-checkout&token=
PAYPAL_URL = "https://www.sandbox.paypal.com/webscr&cmd=_express-checkout&token="



#socket.gethostbyname(socket.gethostname())
#server ip address 174.143.207.130

if socket.gethostbyname(socket.gethostname()) == serveripaddress :
    DOMAIN =".groupalumni.com"
else :
    DOMAIN =".groupalumini2.com:8000"
    
    
    


BATCH_BUCKET_SIZE = 5




#Tag weights
CONTRIBUTION_WEIGHT = 10

PROFILE_WEIGHT = 25

VIEW_WEIGHT = 2



#Stuff related to account activation
ACCOUNT_ACTIVATION_DAYS = 10


#Search Page length
SEARCH_PAGE_SIZE =5


#Profile indicator image
PROFILE_INDICATOR_IMAGE = "profile_indicator"
PROFILE_INDICATOR_EXTENSION = ".png"




#Yahoo browser authentication
CONSUMER_KEY="dj0yJmk9ZzdWd2xHNW44UDR2JmQ9WVdrOVRreE5ZVmxpTkhVbWNHbzlPVEUxTkRreE1EQTUmcz1jb25zdW1lcnNlY3JldCZ4PTdm"
CONSUMER_SECRET="e42c73a431767e09e8673d06d314a9808bce33a0"
APPLICATION_ID="NLMaYb4u"




#feed url
FEED_URL="http://iimjobs.com/index.php?option=com_rd_rss&id=11"











    
    
    














