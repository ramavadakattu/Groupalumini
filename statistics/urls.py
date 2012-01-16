from django.conf.urls.defaults import *


urlpatterns = patterns('statistics.views',
            url(r'^$','displayStatHome',name='displaystathomeurl'),
            url(r'^industrystats/$','showIndustryStats',name='industrystatsurl'),
            url(r'^industrystats/(?P<industryid>\d+)/$','showIndustryMarketStats',name='industrymarketstatsurl'),
            url(r'^departmentstats/$','showDepartmentStats',name='departmentstatsurl'),
            url(r'^departmentstats/(?P<department_id>\d+)/$','showDepartmentCourseStats',name='departmentcoursestatsurl'),
            url(r'^departmentstats/(?P<department_id>\d+)/(?P<course_id>\d+)$','showDegreeStats',name='degreestatsurl'),
            url(r'^batchwisestats/$','showBatchWiseStats',name='batchwisestatsurl'),
        )


#url(r'^(?P<userid>\d+)/$','showProfile',name='profileurl2'),
#url(r'^sendmessage/(?P<touserid>\d+)/$','addShortMessage',name='profilemessageurl'),
#url(r'^postajob/$','postAJob',name='postjoburl'),
#url(r'^postjobcomment/(?P<jobid>[0-9]+)/$','postJobComment',name='postjobcommenturl'),
#url(r'^viewjob/(?P<jobid>[0-9]+)/$','viewJob',name='viewjoburl'),
#url(r'^editjob/(?P<jobid>[0-9]+)/$','editJob',name='editjoburl')