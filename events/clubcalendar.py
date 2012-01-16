from calendar import HTMLCalendar
import calendar
from datetime import date
from itertools import groupby
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from django.utils.html import conditional_escape as esc
from datetime import datetime


class InsituteCalendar(HTMLCalendar):
	
    def __init__(self, events):
        super(InsituteCalendar, self).__init__()
        self.events = self.group_by_day(events)     
    
    def formatmonthname(self, theyear, themonth, withyear=True):   
	return "&nbsp;"
     
   
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = ''
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            
            if  day in self.events.keys():
                cssclass += ' filled'
                if day <  datetime.now().date().day :
                      cssclass += ' past'
                else :
                      cssclass += ' future'
                
                body = ['<ul>']
                for event in self.events[day]:		    
			body.append('<li>')			
			body.append("<a href='%s' > %s </a>  %s at %s"%(event.get_absolute_url(),event.what,event.getTime(),event.where))
                        body.append("<br/>")
                        body.append("Duration : %s %s"%(event.duration,event.durationtag))
                        body.append("<br/>")
			
			#if event.user.get_profile() is not None :
			#    body.append("posted by <a href='%s'>   %s </a>" %(event.user.get_profile().get_absolute_url(),event.user.get_profile().fullname))
			body.append('</li>')
                        
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
	    else :
		return self.day_cell('notfilled', day)
                
        return self.day_cell('noday', '&nbsp;')


    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(InsituteCalendar, self).formatmonth(year, month)
 
	
    def group_by_day(self, events):        
        return dict(
            [(day, list(events)) for day, events in groupby(events, lambda event : event.when.day)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
 

