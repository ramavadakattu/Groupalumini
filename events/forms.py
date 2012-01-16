from events.models import Event
from django import forms
from django.contrib.admin import widgets
from datetime import datetime
from mailgroups.models import MailGroup
import tagging
import re

import logging
import logging.config

mlogger = logging.getLogger(__name__)

   
   
class EventForm(forms.ModelForm):
       #sendemail = forms.BooleanField(required=False,initial=False,label="Would you like to send email to entire alumini")
       tags = tagging.forms.TagField(required=False)
    
       class Meta :
            model = Event
            fields = ('sendemail','what','where','when','starttime','duration','durationtag','description')
            
       def __init__(self, *args , **kwargs):
              user = kwargs['user']
              kwargs.pop('user')
              super(EventForm,self).__init__(*args,**kwargs)              
              self.fields['what'].error_messages['required'] = "Please enter the title of the event"
              self.fields['when'].error_messages['required'] = "Enter the data at which the event will occur"
              self.fields['starttime'].error_messages['required'] = "start time"
              self.fields['duration'].error_messages['required'] = "Please enter the duration of the event"
              self.fields['where'].error_messages['required'] = "You must enter the location of the event"
              self.fields['what'].widget.attrs['size'] = "60"
              self.fields['tags'].widget = forms.widgets.TextInput(attrs={'size':90})
              
              #Add widgets to date and time fields
              self.fields['when'].widget =  widgets.AdminDateWidget()
              self.fields['starttime'].widget = widgets.AdminTimeWidget()
              qualifiers = [ ("hour","hour"),
                   ("hours","hours"),
                   ("days","days"),
                   ("day","day")
                   ]              
              self.fields['durationtag'].choices = qualifiers
              self.fields['durationtag'].initial = "hours"
              
              
              #specify some help text
              self.fields['when'].help_text= 'Date format should be  YYYY-MM-DD'              
              self.fields['starttime'].help_text = "Time format should be HH (24 hours format):MIN:SEC"
              
              self.fields.keyOrder = ['tags','what','when','starttime','where','duration','durationtag','description','sendemail']
              
              self.fields['duration'].widget.attrs['size'] = "8"
              self.fields['where'].widget.attrs['size'] = "25"
              self.fields['where'].help_text = "location of where the event is happening"                            
              self.fields['description'].widget = forms.widgets.Textarea(attrs={'rows':12, 'cols':72})
              
              #intialize sendemail with the user specifc mail groups
              self.fields['sendemail'].queryset = MailGroup.objects.filter(user__id=user.id).order_by("-createddate")
              #self.fields['sendemail'].initial = MailGroup.objects.get(user__id=user.id,entirealumini=True).id
              
              
              
       def clean_when(self):
           """
           Examdate should greater than the current date       
           """            
           when =  self.cleaned_data['when']
           today = datetime.now()
           today_date = today.date()
            
           if when < today_date :            
                raise forms.ValidationError("YOu can't create an event for the past days")
                
           return  self.cleaned_data['when']                 
               





              