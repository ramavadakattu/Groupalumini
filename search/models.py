from django.db import models

import searchsetup
import searchconnect.py

# Create your models here.


# Create your models here.
import logging
import logging.config



mlogger = logging.getLogger(__name__)



mlogger.debug("importing models.....................")


#as the important text is spreaded across different models
#we are creating this temporary models to stuff the content across different models


class SearchDocument(models.Model):
    text = models.TextField()
    passout = models.CharField(max_length=45)
      
    