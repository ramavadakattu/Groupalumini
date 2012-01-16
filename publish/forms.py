from publish.models import Entry
from django import forms
from mailgroups.models import MailGroup
import tagging
import re

import logging
import logging.config

mlogger = logging.getLogger(__name__)



   
   
class PublishForm(forms.ModelForm):
       #sendemail = forms.BooleanField(required=False,initial=False,label="Would you like to send email to entire alumini")
       tags = tagging.forms.TagField(required=False)
    
       class Meta :
            model = Entry
            fields = ('headline','content','sendemail')
            
       def __init__(self, *args , **kwargs):
              editmode = False
              user = kwargs['user']
              kwargs.pop('user')        
              
              if 'editmode' in kwargs.keys() :                
                     editmode = True   
                     kwargs.pop('editmode')
              
              super(PublishForm,self).__init__(*args,**kwargs)              
              self.fields['headline'].error_messages['required'] = "Please enter title of the news Letter......."
              self.fields['content'].error_messages['required'] = "Please enter the content"              
              self.fields['headline'].widget.attrs['size'] = "50"
              self.fields['content'].widget = forms.widgets.Textarea(attrs={'rows':20, 'cols':105})                            
              self.fields['sendemail'].queryset = MailGroup.objects.filter(user__id=user.id).order_by("-createddate")
              self.fields['tags'].widget = forms.widgets.TextInput(attrs={'size':90})
              
              
              if editmode :
                     del self.fields['sendemail']
                     
                     
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
                                   




