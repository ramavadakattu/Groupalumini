from payments.models import Fund,Donation
from django import forms
from django.contrib.admin import widgets

   
   
class FundForm(forms.ModelForm):
    
       class Meta :
            model =  Fund
            fields = ('fundname','totalamount','deadline','description')
            
       def __init__(self, *args , **kwargs):                         
              super(FundForm,self).__init__(*args,**kwargs)              
              self.fields['fundname'].error_messages['required'] = "Please enter the fund name"
              self.fields['totalamount'].error_messages['required'] = "Enter the total amount which you want to raise for this fund"
              self.fields['description'].error_messages['required'] = "Enter the description for the above fund"
              self.fields['fundname'].widget.attrs['size'] = "50"
              self.fields['description'].widget = forms.widgets.Textarea(attrs={'rows':8, 'cols':75})
              
              
              
              self.fields['deadline'].widget =  widgets.AdminDateWidget()
              self.fields['deadline'].error_messages['required'] = "Enter the deadline until which alumini can contribute"
              
              
              
              
              





              
             