from mailgroups.models import MailGroup
from django import forms
from statistics.models import Industry,Market
from datetime import datetime
from institution.models import Department,Course


         
  
class IndustryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name,)
              
              
class MarketChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name,)
              
          
   
   
class MailGroupForm(forms.ModelForm):
    
       class Meta :
            model = MailGroup
            exclude = ('user','entirealumini','institute')
            
       def __init__(self, *args , **kwargs):
              self.institute = kwargs.pop('institute')
              super(MailGroupForm,self).__init__(*args,**kwargs)              
              self.fields['name'].error_messages['required'] = "Please enter the name of this group"
              
              
              #intialize markets and industries
              self.fields['industry'] = IndustryChoiceField(queryset=None)
              self.fields['industry'].queryset = Industry.objects.all()
              self.fields['market'] = MarketChoiceField(queryset=None)
              self.fields['market'].queryset = Market.objects.all()
              self.fields['market'].required = False
              
              self.fields['department'].queryset = Department.objects.filter(institute__id=self.institute.id)
              self.fields['fdepartment'].queryset = Department.objects.filter(institute__id=self.institute.id)
              self.fields['program'].queryset = Course.objects.filter(institute__id=self.institute.id)
              
              self.fields['passoutyear'] = forms.ChoiceField()
              yearlist1 = []
              thisyear = datetime.now().date().year 
              for i in range(1960,thisyear+2):
                     yearlist1.insert(0, (i,i) )
              yearlist1.insert(0,(0,'---'))
              
                     
              self.fields['passoutyear'].initial = "---"           
              self.fields['passoutyear'].choices = yearlist1
              self.fields['passoutyear'].required = False
              self.fields['industry'].required = False
              
         
      
              





              
             