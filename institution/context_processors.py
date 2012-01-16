from institution.models import Institution
import urlparse
import settings


def get_institute(request):
    """
    THe main aim of this context processor is to fill the institute for a given request object
    if institute object is None it means the site is running on the main site
    """      
    request.institute = None       
    subdomain = None
    parts =  request.get_host().split(".")
    homeurl = None
    if len(parts) == 3:
        subdomain = parts[0]
        
    if subdomain is None or subdomain == "www" or len(parts) == 2:
        institute = None       
    else:
        try :            
            institute = Institution.objects.get(subdomain__iexact = subdomain)
            #ALso let us send Insitute home url
            homeurl = institute.getInstituteHomeUrl()
            return {'institute':institute,'map_api_key':settings.maps_api_key,'homeurl':homeurl}
        except :
            #later we will figure it our what to do
            pass
                
    return {'institute':None,'homeurl':homeurl}   
          
    
