from django.conf.urls.defaults import *


urlpatterns = patterns('interesting.views',
        url(r'^$','displayHome',name='interestinghome'),
        url(r'^submittags/$','submitTags',name='submittagsurl'),
        url(r'^taglookup/$','tagLookup',name='taglookupurl'),
        url(r'^getpeople/$','getInterestingPeople',name='interestingpeopleurl'),
         url(r'^getcontent/$','getInterestingContent',name='interestingcontenturl'),
         url(r'^jobs/$','getInterestingJobs',name='interestingjobsurl'),
         url(r'^events/$','getInterestingEvents',name='interestingeventsurl'),
         url(r'^discuss/$','getInterestingDiscussions',name='interestingdiscussurl'),
         url(r'^research/$','getInterestingResearchPapers',name='interestingresearchurl'),        
        )