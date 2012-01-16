from django.conf.urls.defaults import *
import dev_settings
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
     (r'^$', include('institution.urls')),     
     (r'^institution/', include('institution.urls')),
     (r'^askalumini/', include('askalumini.urls')),
     (r'^profile/', include('profile.urls')),     
     (r'^search/', include('search.urls')),
     (r'^location/', include('location.urls')),
     (r'^jobs/', include('jobs.urls')),
     (r'^events/', include('events.urls')),
     (r'^payments/', include('payments.urls')),
     (r'^blog/', include('publish.urls')),
     (r'^feedback/', include('feedback.urls')),
     (r'^fetchcontacts/', include('fetchcontacts.urls')),
     (r'^interesting/', include('interesting.urls')),
     (r'^connections/', include('connections.urls')),
     (r'^mailgroups/', include('mailgroups.urls')),
     (r'^statistics/', include('statistics.urls')),     
     (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
     
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)




#For static pages
urlpatterns += patterns('django.views.generic.simple',
						url(r'^home/$','direct_to_template',{'template':'alumclub_home.html'},name="homeurl"),
						url(r'^features/$','direct_to_template',{'template':'features.html'},name="featuresurl"),
						url(r'^about/$','direct_to_template',{'template':'about_alumclub.html'},name="abouturl"),
						url(r'^contact/$','direct_to_template',{'template':'contact.html'},name="contacturl"),
                        url(r'^googlehostedservice.html$','direct_to_template', {'template':'googlehostedservice.html'}, name="googleappurl"),
                         url(r'^PAMQzhNCZCcoUeWI8TFOeQ--.html$','direct_to_template', {'template':'PAMQzhNCZCcoUeWI8TFOeQ--.html'}, name="yahooappurl")
                        
                       )   


if dev_settings.DEBUG :    
    urlpatterns += patterns('',
            url(r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )

