from django.conf.urls.defaults import *


urlpatterns = patterns('mailgroups.views',
            url(r'^$','displayMailGroups',name='displaymailgroupurl'),            
            url(r'^create/$','createMailGroup',name='createmailgroupurl'),            
            url(r'^delete/(?P<mailgroupid>[0-9]+)/$','deleteMailGroup',name='deletemailgroupurl'),
            url(r'^edit/(?P<mailgroupid>[0-9]+)/$','editMailGroup',name='editmailgroupurl')
          )

