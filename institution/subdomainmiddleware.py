from institution.models import Institution
import urlparse

import logging
import logging.config



mlogger = logging.getLogger(__name__)

class SubdomainMiddleware:
      """
      THe main aim of this middleware is to fill the institute for a given request object
      if institute object is None it means the site is running on the main site
      """      
      def process_request(self, request):      
        request.institute = None       
        subdomain = None
        parts =  request.get_host().split(".")
        if len(parts) == 3:
            subdomain = parts[0]
        mlogger.debug("what wrong = %s"%( urlparse.urlsplit(request.get_host()),))
        mlogger.debug("parts = %s, %s , %s"% (str(parts),request.get_host(),urlparse.urlsplit(request.get_host())[0]))
        if subdomain is None or subdomain == "www" or len(parts) == 2:
            request.institute = None
            mlogger.debug("subdomain is None ...................")
            return None
        else:
            try :            
               request.institute = Institution.objects.get(subdomain__iexact = subdomain)
               mlogger.debug("subdomain is %s"%subdomain)
            except :
                #later we will figure it our what to do
                pass
                
        return None   
        
