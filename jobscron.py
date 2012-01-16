
from django.core.management import setup_environ
import settings
setup_environ(settings)

import logging
import feedparser
from jobs.models import Job
import datetime


mlogger = logging.getLogger(__name__)




   
def fetchFromFeed():
    feedurl = settings.FEED_URL
    mlogger.debug("Fetching new jobs from feedurl.................................")
    d = feedparser.parse(settings.FEED_URL)
    latestjob  =  Job.objects.filter(viafeed=True).order_by('-viafeeddatetime')[:1]    
   
    for entry in  d['entries'] :
         
        #post each job into the admin
        title = entry['title']
        description = entry['description']
        link = entry['link']
        description =  description + "<br/> <br/> More information : <br/> "  + link 
        date = datetime.datetime(*entry['date_parsed'][:6])

        
        if  len(latestjob) == 0 or (date  > latestjob[0].viafeeddatetime) :
            #for each job
            mlogger.debug("saving a job")
            j = Job()
            j.title = title
            j.description = description
            j.viafeed = True
            j.viafeeddatetime = date            
            j.save()
            
        
fetchFromFeed()        
        