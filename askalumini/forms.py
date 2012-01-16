from django import forms
from askalumini.models import Question , Answer
import settings
from django.utils.html import mark_safe
import tagging
import re

import logging
import logging.config

mlogger = logging.getLogger(__name__)


class QuestionForm(forms.ModelForm) :
       ''' Form which allows institutions to register'''
       tags = tagging.forms.TagField(required=False)
       
       class Meta :
            model = Question
            fields = ('subject', 'description')
                     
      
       def __init__(self, *args , **kwargs):
            super(QuestionForm,self).__init__(*args,**kwargs)            
            self.fields.keyOrder = ['subject','description','tags']            
            self.fields['subject'].error_messages['required'] = "Please enter the title of the question"
            self.fields['subject'].label = ""
            self.fields['subject'].widget = forms.widgets.TextInput(attrs={'size':82})           
            self.fields['tags'].widget = forms.widgets.TextInput(attrs={'size':90})
            self.fields['description'].error_messages['required'] = "PLease enter the description of the question"
            self.fields['description'].label = ""
            self.fields['description'].widget = forms.widgets.Textarea(attrs={'id':'wmd-input','class':'wmd-panel','rows':15, 'cols':92})
            
            
            
       def clean_tags(self):
            mlogger.debug("Make sure it contatins only alpahnumeric characters")
            tags = self.cleaned_data['tags'].strip()
            if len(tags) == 0 :
              return self.cleaned_data['tags']
            #make sure that the tags are of valid string
            e = re.compile(r"[0-9A-Za-z-. ]+",re.IGNORECASE)
            result = e.match(tags)    
            if result is not None  and len(tags) == result.span()[1] :
              return self.cleaned_data['tags']
            else :
              raise forms.ValidationError("Error:Tags should only contain alphanumeric characters, space,hypen('-'),dot('.'). Tags shoud be saperated by space")
              
            
            
           
class AnswerForm(forms.ModelForm):
    ''' Form which allows the user to post answer'''
    
    class Meta :
        model = Answer
        fields = ('text',)
        
        
    def __init__(self,*args , **kwargs):
            super(AnswerForm,self).__init__(*args,**kwargs) 
            self.fields.keyOrder = ['text']            
            self.fields['text'].error_messages['required'] = "Please enter your answer to this question"
            self.fields['text'].label = ""           
            self.fields['text'].widget = forms.widgets.Textarea(attrs={'id':'wmd-input','class':'wmd-panel','rows':15, 'cols':92})
        
           
            
            
            
           