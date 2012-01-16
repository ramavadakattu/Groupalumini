from django.conf.urls.defaults import *


urlpatterns = patterns('profile.views',
        url(r'^$','showProfile',name='profileurl'),
        url(r'^(?P<userid>\d+)/$','showProfile',name='profileurl2'),
        url(r'^sendmessage/(?P<touserid>\d+)/$','addShortMessage',name='profilemessageurl'),
       )
