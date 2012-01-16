from django.conf.urls.defaults import *


urlpatterns = patterns('events.views',
            url(r'^$','getAgendaView',name='eventhomeurl'),            
            url(r'^agenda/$','getAgendaView',name='agendaviewurl'),
            url(r'^createevent/$','createEvent',name='createeventurl'),
            url(r'^viewevent/(?P<eventid>[0-9]+)/$','viewEvent',name='vieweventurl'),
            url(r'^editevent/(?P<eventid>[0-9]+)/$','editEvent',name='editeventurl'),
            url(r'^deleteevent/(?P<eventid>[0-9]+)/$','deleteEvent',name='deleteeventurl'),
            url(r'^calendar/$','getCalendarView',name='calendarviewurl'),
            url(r'^calendar/(?P<month>\d{1,2})/(?P<year>\d{4})/$','getCalendarView',name='calendarviewurl2'),
            url(r'^attending/(?P<eventid>[0-9]+)/(?P<attendingflag>[0-9]+)/$','trackAttendence',name='eventattendurl'),
            
            
            
            #url(r'^month/(?P<month>\d{1,2})/(?P<year>\d{4})/$','displayMonthlyView',name='monthviewurl2'),        
          )
