from django.conf.urls.defaults import *


urlpatterns = patterns('search.views',
        url(r'^$','alumClubSearch',name='searchurl'),
        url(r'page(?P<pageno>[0-9]+)/$','alumClubSearch',name='searchurl2' )
       )
