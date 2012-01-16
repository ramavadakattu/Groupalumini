from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User 
from django.contrib.auth.backends import ModelBackend
from django.db.models import get_model
from django.utils.html import escape


import logging

mlogger = logging.getLogger(__name__)

class EmailBackEnd(ModelBackend):
    
    def authenticate(self, email=None, password=None):                           
                mlogger.debug("Hello iam doing authentication")                
               
                try:                   
                    #he entered email authenticate with email                        
                    user = User.objects.get(email=email)                                            
                    #Did he entered valid password
                    if user.check_password(password):
                        return user
                    else :
                        return None
                    
                except User.DoesNotExist :                                              
                    return None
                
                
  
        
        
                  
                
      