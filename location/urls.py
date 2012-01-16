from django.conf.urls.defaults import *


urlpatterns = patterns('location.views',
            url(r'^$','locateHome',name='locateurl'),
            url(r'^(?P<ncountryname>[a-zA-Z0-9-]+)/$','browseByCountry',name='countryurl'),
            url(r'^(?P<ncountryname>[a-zA-Z0-9-]+)/(?P<nstatename>[a-zA-Z0-9-]+)/$','browseByState',name='stateurl'),
            url(r'^(?P<ncountryname>[a-zA-Z0-9-]+)/(?P<nstatename>[a-zA-Z0-9-]+)/(?P<pageno>[0-9]+)/$','browseByState',name='statepageurl'),
            
            
          )


#url(r'^(?P<userid>\d+)/$','showProfile',name='profileurl2'),
#url(r'^sendmessage/(?P<touserid>\d+)/$','addShortMessage',name='profilemessageurl'),