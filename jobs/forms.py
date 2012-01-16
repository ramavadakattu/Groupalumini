from jobs.models import Job,JobComment
from django import forms
from mailgroups.models import MailGroup
import tagging
import re

import logging
import logging.config

mlogger = logging.getLogger(__name__)

   
   
class JobForm(forms.ModelForm):
       tags = tagging.forms.TagField(required=False)
       
       class Meta :
            model = Job
            fields = ('title','description','location','sendemail')
            
       def __init__(self, *args , **kwargs):
              user = kwargs['user']
              kwargs.pop('user')
              
              super(JobForm,self).__init__(*args,**kwargs)              
              self.fields['title'].error_messages['required'] = "Please enter the title of the job"
              self.fields['description'].error_messages['required'] = "Additonal description please...."
              self.fields['location'].error_messages['required'] = "Please enter the job posting location"
              self.fields['title'].widget.attrs['size'] = "50"
              self.fields['description'].widget = forms.widgets.Textarea(attrs={'id':'wmd-input','class':'wmd-panel','rows':15, 'cols':92})              
              self.fields['sendemail'].queryset = MailGroup.objects.filter(user__id=user.id).order_by("-createddate")
              self.fields['tags'].widget = forms.widgets.TextInput(attrs={'size':90})
              
              
       def clean_tags(self):
            mlogger.debug("Make sure it contatins only alpahnumeric characters")
            tags = self.cleaned_data['tags'].strip()    
            #make sure that the tags are of valid string
            if len(tags) == 0 :
              return self.cleaned_data['tags']
              
            #if he enters any things make sure it contains only alpha numeric characters            
            e = re.compile(r"[0-9A-Za-z-. ]+",re.IGNORECASE)
            result = e.match(tags)    
            if result is not None  and len(tags) == result.span()[1] :
              return self.cleaned_data['tags']
            else :
              raise forms.ValidationError("Error:Tags should only contain alphanumeric characters, space,hypen('-'),dot('.'). Tags shoud be saperated by space")
              
            




              
             