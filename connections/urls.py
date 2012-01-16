from django.conf.urls.defaults import *


urlpatterns = patterns('connections.views',
        url(r'^$','displayConnections',name='connectionhome'),
        url(r'^add/(?P<touserid>[0-9]+)/$','addConnection',name='newconnectionurl'),
        url(r'^delete/(?P<connectionid>[0-9]+)/$','deleteConnection',name='deleteconnectionurl'),
         url(r'^accept/(?P<connectionid>[0-9]+)/$','acceptConnection',name='acceptconnectionurl'),
        url(r'^pending/$','pendingConnections',name='pendingconnectionurl'),                  
        )