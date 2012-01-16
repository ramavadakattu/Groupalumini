from django.conf.urls.defaults import *


urlpatterns = patterns('jobs.views',
            url(r'^$','displayJobs',name='displayjoburl'),            
            url(r'^postajob/$','postAJob',name='postjoburl'),
            url(r'^postjobcomment/(?P<jobid>[0-9]+)/$','postJobComment',name='postjobcommenturl'),
            url(r'^viewjob/(?P<jobid>[0-9]+)/$','viewJob',name='viewjoburl'),
            url(r'^editjob/(?P<jobid>[0-9]+)/$','editJob',name='editjoburl'),
            url(r'^deletejob/(?P<jobid>[0-9]+)/$','deleteJob',name='deletejoburl')
          )


#url(r'^(?P<userid>\d+)/$','showProfile',name='profileurl2'),
#url(r'^sendmessage/(?P<touserid>\d+)/$','addShortMessage',name='profilemessageurl'),