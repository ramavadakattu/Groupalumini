from django.conf.urls.defaults import *
from publish.models import Entry
from django.views.generic import date_based, list_detail
import settings
from feeds import LatestInstituteBlogPosts




urlpatterns = patterns('publish.views',
            url(r'^$','displayNewsLetters',name='newsletterurl'),
            url(r'^entry(?P<entry_id>[0-9]+)/$','displaySinglePost',name='singleposturl'),
            url(r'^archives/$','displayArchives',name='archiveurl'),
            url(r'^postcomment/(?P<entry_id>[0-9]+)/$','postComment',name='postcommenturl'),
             url(r'^postnewentry/$','publishNewsLetter',name='publishnewurl'),
             url(r'^postnewentry/(?P<entry_id>[0-9]+)/$','publishNewsLetter',name='publishnewurl2'),
             url(r'^editentry/(?P<entry_id>[0-9]+)/$','editEntry',name='editentryurl'),
             url(r'^myposts/$','getMyPosts',name="mypostsurl"),
             url(r'^delete/(?P<entry_id>[0-9]+)/$','deleteEntry',name='deleteentryurl'),
             url(r'^faculty/(?P<faculty_name>[0-9A-Za-z-]+)/$','displayFacultyResearch',name='facultyresearchurl'),
             url(r'^faculty/archives/(?P<faculty_name>[0-9A-Za-z-]+)/$','displayResearchArchive',name='facultyarchiveurl'),
              url(r'^rfaculty/publish/$','publishNewResearch',name='researchnewurl'),
              url(r'^rfaculty/publish/(?P<entry_id>[0-9]+)/$','publishNewResearch',name='researchnewurl2'),
              url(r'^rfaculty/edit/(?P<entry_id>[0-9]+)/$','editPaper',name='editpaperurl'),
              url(r'^rfaculty/entry/(?P<entry_id>[0-9]+)/$','displaySinglePaper',name='singlepaperurl'),
              url(r'^rfaculty/delete/(?P<entry_id>[0-9]+)/$','deletePaper',name='deletepaperurl'),
             
             
          )




feeds = {
   'latest': LatestInstituteBlogPosts,
   
}


urlpatterns += patterns('',
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='institute_feed_url') ,
                    
                    
                        )






#url(r'^(?P<userid>\d+)/$','showProfile',name='profileurl2'),
#url(r'^sendmessage/(?P<touserid>\d+)/$','addShortMessage',name='profilemessageurl'),