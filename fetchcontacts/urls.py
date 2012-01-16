from django.conf.urls.defaults import *


urlpatterns = patterns('fetchcontacts.views',
            url(r'^$','fetchContactsHome',name='invitehomeurl'),
            url(r'^gmail/$','fetchGmailContacts',name='gmailcontactsurl'),
             url(r'^yahoo/$','fetchYahooContacts',name='yahoocontactsurl'),
              
       )
