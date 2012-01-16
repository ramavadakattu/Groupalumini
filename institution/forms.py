from institution.models import Institution
import re

from django import forms
from django.contrib.auth.models import User
from institution.models import Student , Faculty , Department , Course , Institution ,Degree
from django.contrib.auth import authenticate
from datetime import datetime
from location.models import Country,State

from statistics.models import Industry,Market




class IRegForm(forms.ModelForm) :
       ''' Form which allows institutions to register'''
       adminemail = forms.CharField(max_length=100,required=True,help_text="we will be occasionally communicating via this email")
       adminname = forms.CharField(max_length=100,label="Admin Name",required=True)
       password1 = forms.CharField(max_length=30,label="Password",widget=forms.PasswordInput,required=True)
       password2 = forms.CharField(max_length=30,label="Retype password",widget=forms.PasswordInput,required=True)
       logo = forms.ImageField()
       editmode = 0
       
       class Meta :
            model = Institution
            exclude = ('admin',)
                     
      
       def __init__(self, editmode , *args , **kwargs):
            super(IRegForm,self).__init__(*args,**kwargs) 
            self.fields.keyOrder = ['name','website','phoneno','logo','description','subdomain','adminemail','adminname','password1','password2']
            
            self.fields['password1'].error_messages={'required':'Please enter password'}
            self.fields['password2'].error_messages={'required':'Please retype your password'}
            self.fields['adminemail'].error_messages={'required':'Please enter admin email','invalid':'Invalid email'}            
            self.fields['phoneno'].error_messages={'required':'Please enter institute phone number'}
            self.fields['website'].error_messages={'required':'Please retype your password','invalid':'Invalid URL'}
            self.fields['subdomain'].error_messages={'required':'Please enter the subdomain at which you want your alumini network'}
            self.fields['name'].error_messages={'required':'Please enter institution name'}
            self.fields['adminname'].error_messages['required'] = "Please enter the admin name"
            self.fields['logo'].error_messages['required'] = "You should enter the logo of your institute"
            
            if editmode > 0 :
              del self.fields['logo']
              del self.fields['password1']
              del self.fields['password2']
              self.editmode = editmode
              
        
       def clean_subdomain(self):
           """
           Validates that the Subdomain should not contain characters other than alphabets,digits
           """
           #make sure that this field is alphanumeric
           k = re.compile(r'[1-9]*[a-zA-Z][0-9A-Za-z]*')
           only_number = re.compile(r'[0-9]+')
           
           if not k.match(self.cleaned_data['subdomain']) :
              if only_number.match(self.cleaned_data['subdomain']) :             
                    raise forms.ValidationError('Atleast one alphabet...............')
                    
              raise forms.ValidationError('Only letters and numbers are allowed. (spaces,-,_ etc not allowed ,Starting character should not be 0')
           else :
              result = []
              if self.editmode > 0 :
                  result = Institution.objects.exclude(id=self.editmode).filter(subdomain__iexact=self.cleaned_data['subdomain'])  
              else :         
                  result = Institution.objects.filter(subdomain__iexact=self.cleaned_data['subdomain'])
              if len(result) > 0:
                   raise forms.ValidationError("This subdomain is already registered by Insitute >> %s" %(result[0].name,))
              
              return self.cleaned_data['subdomain']
              
                     
       def clean_adminemail(self):
              ''' Make sure admin email are  unique'''
              try :
                     if self.editmode > 0 :
                            admin = Institution.objects.get(id=self.editmode).admin
                            u = User.objects.exclude(id=admin.id).get(email=self.cleaned_data['adminemail'])
                     else :
                            u = User.objects.get(email=self.cleaned_data['adminemail'])
                            
                            
                     raise forms.ValidationError('Email address is already registered with alumclub ,Please choose another email')
              except User.DoesNotExist:
                     return self.cleaned_data['adminemail']
              
                 
         
       def clean(self):
              if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
                     if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                            raise forms.ValidationError('Admin passwords did  not match Please type again')
                            
                                          
                            
              return self.cleaned_data
 
import logging
import logging.config
       
mlogger = logging.getLogger(__name__)
class LoginForm(forms.Form) :
    ''' As our needs are to make user to enter email / username we are writing a sample
        authentication form which caters those needs.'''        
    email = forms.RegexField(max_length=30,label='Email',regex=r'^[a-zA-Z0-9._@]+',error_messages={'required':'Please enter your  email','invalid':'@,_,. and alphanumeric characters are only allowed for the field email'})               
    password = forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Please enter your password'})
   
        
    def __init__(self, institute, *args , **kwargs):
          super(LoginForm,self).__init__(*args,**kwargs)
          self.institute = institute
    
    def clean(self):        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
          
        if email and password :
	     user = authenticate(email=email, password=password)
             if user is None :                
                #finding the proper error messages
                u = None
                error = None
		try:
                    u = User.objects.get(email=email)                    
                except User.DoesNotExist :
		    error = "This email  is not registed with alumclub"  
                
                if u is None :
                    raise forms.ValidationError(error)
                else:
                    if not u.check_password(password):
                        raise forms.ValidationError("Email and password do not match")
             elif user is not None :
		     mlogger.debug(" approved  is %s"% user.get_profile().approved)
                     #Make sure this user below to this institute
                     profile = user.get_profile()
                     if self.institute not in profile.institutes.all() :                            
                            raise forms.ValidationError("Your are not the user of this institute.............")                        
                                   
                     if not user.get_profile().emailverified :
                             raise forms.ValidationError("Your have not verified your email")                        
                     elif user.get_profile().approved == 0 :
                        # if not user.get_profile().isadmin :
                             #raise forms.ValidationError("Your institute admin has not activated the acccount.Please contact your admin.......")
                       if user.get_profile().isadmin :
                             #Make sure institute account is activated                                          
                             institute = Institution.objects.get(admin__email=email.strip())
                             if not  institute.active  :
                                    raise forms.ValidationError("Institute account has not been activated please contact our support")
		     elif user.get_profile().approved == -1 :
			     raise forms.ValidationError("You profile has been rejected by the institute admin.Please contact our support.")
                                    
            
                
        return self.cleaned_data
       
       
class FacultyForm(forms.ModelForm):
       institutename = forms.CharField(max_length=1024,required=True)
       name = forms.CharField(max_length=40,required=True)
       email = forms.RegexField(max_length=30,label='Email',regex=r'^[a-zA-Z0-9._@]+',error_messages={'required':'Please enter your  email','invalid':'@,_,. and alphanumeric characters are only allowed for the field email'})               
       password = forms.CharField(max_length=30,widget=forms.PasswordInput,help_text="<a href=\"/smauth/resetpassword/\"/> Forgot my password! </a>",error_messages={'required':'Please enter your password'})
       retype_password = forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Please retype your password'})
       '''
       country = forms.ModelChoiceField(queryset=None,empty_label=None)
       state = forms.CharField(max_length=200)
       city = forms.CharField(max_length=100,required=False,initial="")
       address = forms.CharField(max_length=3000,required=False,initial="")
       latitude = forms.FloatField(widget=forms.HiddenInput())
       longitude = forms.FloatField(widget=forms.HiddenInput())'''
       department = forms.ModelChoiceField(queryset = None,empty_label=None)
       editmode = 0
       
       class Meta :
            model = Faculty
            exclude = ('institutes','profile','specialization','designation','subjects')
            
       def __init__(self, instituteid, editmode, *args , **kwargs):                         
              super(FacultyForm,self).__init__(*args,**kwargs)
              #prefill the institute name with institute
              institute = Institution.objects.get(pk=instituteid)
              if institute is not None :
                  self.fields['institutename'].initial = institute.name
                  self.fields['institutename'].widget.attrs['readonly'] = True
              self.fields['name'].error_messages['required'] = "Please enter your name"
              #self.fields['subjects'].error_messages['required'] = "Please enter the subjects which you have taught"
              #self.fields['specialization'].error_messages['required'] = "What is your area of specialization?"
              #self.fields['designation'].error_messages['required'] = "Please enter your designation at this institute"
              self.fields['institutename'].error_messages['required'] = "Your should enter institute name"
              
              
              '''self.fields['country'].widget.attrs['id'] =  "country2"
              self.fields['city'].widget.attrs['id'] = "city2"
              self.fields['state'].widget.attrs['id'] = "state2"
              self.fields['longitude'].widget.attrs['id'] = "longitude2"
              self.fields['longitude'].initial = 0
              self.fields['latitude'].widget.attrs['id'] = "latitude2"
              self.fields['latitude'].initial = 0
              self.fields['address'].widget.attrs['id'] = "address2"'''
              
              #intialize drop dowsn for COuntry and state
              #self.fields['country'].queryset = Country.objects.all().order_by("name")             
              #self.fields['state'].queryset = State.objects.all().order_by("-name")
              
              
              #configure error messages for the location attributes
              ''' self.fields['country'].error_messages['required'] = "You  should enter the country name"
              self.fields['city'].error_messages['required'] = "You should enter the city name"
              self.fields['state'].error_messages['required'] = "You should enter the state name" '''
             
              
              
              #increase the size of address field
              #self.fields['address'].widget.attrs['size'] = 50
              
              #intialize the queryset for the course and department fields          
              self.fields['department'].queryset = institute.department_set.all().order_by('name')
              self.fields['department'].error_messages['required'] = "Please enter the department in which you are working"
              self.fields['department'].widget.attrs['id'] = "fdepartment"
              
              
              #self.fields.keyOrder = ['longitude','department','latitude','country','state','city','address','email','password','name','website','institutename','subjects','specialization','designation']
              
              
              if editmode > 0 :                   
                   del self.fields['password']
                   del self.fields['retype_password']
                   self.editmode = editmode
                     
              
       def clean_email(self):
              ''' Make sure the email is unique take note of editing a field'''
              try :
                     if self.editmode > 0 :
                            u = User.objects.exclude(id=self.editmode).get(email=self.cleaned_data['email'])
                     else :
                            u = User.objects.get(email=self.cleaned_data['email'])                     
                     raise forms.ValidationError('Email address is already registered with alumclub ,Please choose another email')
              except User.DoesNotExist:
                     return self.cleaned_data['email']
                     
                     
       def clean(self):
              if 'password' in self.cleaned_data and 'retype_password' in self.cleaned_data:                    
                     if self.cleaned_data['password'] != self.cleaned_data['retype_password']:
                            raise forms.ValidationError('Passwords did  not match Please type again')                           
                                          
                            
              return self.cleaned_data
 
                            
              
  
class IndustryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name,)
              
              
class MarketChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name,)
              
              
              
       
class StudentForm(forms.ModelForm):
       name = forms.CharField(max_length=40,required=True)
       email = forms.RegexField(max_length=30,label='Email',regex=r'^[a-zA-Z0-9._@]+',error_messages={'required':'Please enter your  email','invalid':'@,_,. and alphanumeric characters are only allowed for the field email'})               
       password = forms.CharField(max_length=30,widget=forms.PasswordInput,help_text="<a href=\"/smauth/resetpassword/\"/> Forgot my password! </a>",error_messages={'required':'Please enter your password'})
       retype_password = forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Please retype your password'})
       institutename = forms.CharField(max_length=1024,required=True)
       fromyear =  forms.ChoiceField()
       toyear = forms.ChoiceField(required=False,help_text="<a href='#'> if you have not passed out then leave it as blank</a>")       
       course = forms.ModelChoiceField(queryset = None,empty_label=None)
       department = forms.ModelChoiceField(queryset = None,empty_label=None)
       degree = forms.ModelChoiceField(queryset = None,empty_label=None)       
       
       '''country = forms.ModelChoiceField(queryset=None,empty_label=None)
       state = forms.CharField(max_length=200)
       city = forms.CharField(max_length=100,required=False,initial="")
       address = forms.CharField(max_length=3000,required=False,initial="")     
       latitude = forms.FloatField(widget=forms.HiddenInput())
       longitude = forms.FloatField(widget=forms.HiddenInput())'''
       
       
       editmode = 0
      
       alignwithprevious = ['toyear']
      
       class Meta :
            model = Student
            exclude = ('institutes','profile','whatiamdoing','company','title','industry','market')            
            
       def __init__(self, instituteid, editmode, *args , **kwargs):              

              super(StudentForm,self).__init__(*args,**kwargs)
              #prefill the institute name with institute
              
              institute = Institution.objects.get(pk=instituteid)              
              if institute is not None :
                     self.fields['institutename'].initial = institute.name
                     self.fields['institutename'].widget.attrs['readonly'] = True

              #self.fields['industry'].choices  = [("",'--'),('Internet','internet'),('Civil engineering','Civil Engineering')]
              
              #Prefill the choices for fromyear and toyear
              yearlist1 = [("",'---')]
              yearlist = []
              for i in range(1960,2021):
                     yearlist1.insert(0, (i,i) )
                     yearlist.insert(0, (i,i) )
              
              thisyear  =   datetime.now().date().year     
                     
              self.fields['toyear'].choices = yearlist
              self.fields['toyear'].initial = ""
              self.fields['fromyear'].choices = yearlist
              self.fields['fromyear'].initial = thisyear
              
              
              #Customize error message
              self.fields['name'].error_messages['required'] = "Please enter your name"
              self.fields["name"].temp_value = 2
             
              self.fields['fromyear'].error_messages['required'] = "Year from which you are studing in the institute"       
             
              self.fields['institutename'].error_messages['required'] = "Your should enter institute name"
              self.fields['course'].error_messages['required'] = "Please enter the course which you have studied in this institute"             
              #self.fields.keyOrder = ['longitude','latitude','country','state','city','address','email','password','name','website','institutename','fromyear','toyear','course','department','whatiamdoing','company','title','industry','market','degree']
                         
              
              #increase the size of address field
              '''self.fields['address'].widget.attrs['size'] = 50
              self.fields['country'].widget.attrs['id'] =  "country1"
              self.fields['country'].queryset = Country.objects.all().order_by("name")
              self.fields['city'].widget.attrs['id'] = "city1"
              self.fields['state'].widget.attrs['id'] = "state1"
              #self.fields['state'].queryset = State.objects.all().order_by("-name")
              self.fields['address'].widget.attrs['id'] = "address1"
              self.fields['longitude'].widget.attrs['id'] = "longitude1"
              self.fields['latitude'].widget.attrs['id'] = "latitude1"               
              self.fields['longitude'].initial = 0              
              self.fields['latitude'].initial = 0'''
              
              
              #configure error messages for the location attributes
              '''self.fields['country'].error_messages['required'] = "You  should enter the country name"
              self.fields['city'].error_messages['required'] = "You should enter the city name"
              self.fields['state'].error_messages['required'] = "You should enter the state name"'''
              
             
              
              #intialize the queryset for the course and department fields
              #assert False
              departments = institute.department_set.all().order_by('name')
              self.fields['department'].queryset = departments
              degrees = Degree.objects.filter(institute__id=institute.id).order_by("-name")
              self.fields['degree'].queryset = degrees
              self.fields['degree'].error_messages['required'] = "Please enter the degree"
              
              self.fields['course'].queryset = institute.course_set.all().order_by('name')                     
              self.fields['department'].error_messages['required'] = "Please enter the department in which you are working"
              self.fields['department'].widget.attrs['id'] = "sdepartment"
              self.fields['course'].error_messages['required'] = "Please enter the course which you have taken at the institute"
              
              
              
              #intialize markets and industries
              #self.fields['industry'] = IndustryChoiceField(queryset=None)
              #self.fields['industry'].queryset = Industry.objects.all()
              #self.fields['market'] = MarketChoiceField(queryset=None)
              #self.fields['market'].queryset = Market.objects.all()              
              
                            
              if editmode > 0 :                  
                   del self.fields['password']
                   del self.fields['retype_password']
                   self.editmode = editmode
                   
             
              
       def clean_email(self):
              ''' Make sure the email is unique'''              
              try :
                     if self.editmode > 0 :
                            u = User.objects.exclude(id=self.editmode).get(email=self.cleaned_data['email'])
                     else :
                            u = User.objects.get(email=self.cleaned_data['email'])                     
                     raise forms.ValidationError('Email address is already registered with alumclub ,Please choose another email')
              except User.DoesNotExist:
                     return self.cleaned_data['email']
              
                     
                     
       def clean(self):
              ''' make sure what he selected matches fields he filled'''       
              
              #verify the below only if self.cleaned_data['whatiamdoing']       
              ''' option = self.cleaned_data['whatiamdoing'].lower() 
              if option == "employee" :
                   #All three must be filled
                   if len(self.cleaned_data['company'].strip()) <= 0:                     
                      self.errors['company'] = forms.util.ErrorList([u"Please enter company name"])
                   if len(self.cleaned_data['title'].strip()) <= 0:                       
                       self.errors['title'] = forms.util.ErrorList([u"Please enter the title you have at your office"])
                   if self.cleaned_data['industry'] is None  :
                       self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                   if self.cleaned_data['market'] is None  :
                       self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])    
              elif option == "owner" :                     
                     if len(self.cleaned_data['company'].strip()) <= 0:                     
                            self.errors['company'] = forms.util.ErrorList([u"Please enter company name"])
                     if self.cleaned_data['industry'] is None :
                            self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                     if self.cleaned_data['market'] is None  :
                       self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])           
              elif option == "lwork" or option == "freelance" :
                        if self.cleaned_data['industry'] is None :
                            self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                        if self.cleaned_data['market'] is None  :
                            self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])'''                          
               
              if 'password' in self.cleaned_data and 'retype_password' in self.cleaned_data:
                     if self.cleaned_data['password'] != self.cleaned_data['retype_password']:
                            raise forms.ValidationError('Passwords did  not match Please type again')                           
                                          
                            
              return self.cleaned_data                                            
                 
                     
                     
              
              
class ImageUploadForm(forms.Form):
       newphoto = forms.ImageField(label="New Image")
      
       def __init__(self, *args , **kwargs):
              super(ImageUploadForm,self).__init__(*args,**kwargs)
              self.fields['newphoto'].error_messages['required'] = "Please enter the image to be uploaded........."
              
              





class ChangePasswordForm(forms.Form) :
    old_password =  forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Please enter your old password'})
    new_password =  forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Please enter your new password'})
    retye_new_password =  forms.CharField(max_length=30,widget=forms.PasswordInput,error_messages={'required':'Retype your new password'})
    userid = None
     

    #dynamic forms adding and removing property as required 	
    def __init__(self,userid , *args , **kwargs):        
	super(self.__class__,self).__init__(*args,**kwargs)
        self.userid=userid
        self.fields['retye_new_password'].label = "Retype Password"
	    


    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        non_field_errors() because it doesn't apply to a single
        field.
        
        """
        user = User.objects.get(pk = self.userid)   
           	
	if 'old_password' in self.cleaned_data :
	    if not user.check_password(self.cleaned_data['old_password']) :
         	raise forms.ValidationError('Your old password is invalid')
	
        if 'new_password' in self.cleaned_data and 'retye_new_password' in self.cleaned_data:	    
            if self.cleaned_data['new_password'] != self.cleaned_data['retye_new_password']:
                raise forms.ValidationError('You must type the same new password each time')       
         		
		
        return self.cleaned_data  
              
              
       
       

class ForgotPasswordForm(forms.Form) :
    email =   forms.EmailField(max_length=50,error_messages={'required':'Please enter your email'},help_text='Your new password will be sent to this mail')
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """	
	if 'email' in self.cleaned_data :
	    #check does this email exists in the database
	    try:
	        user =   User.objects.get(email=self.cleaned_data['email'])
	    except User.DoesNotExist :
                raise forms.ValidationError('WE presently do not have any registered account with this email.Please check your email address.')	 
	return self.cleaned_data
       
       



 
   
class DepartmentForm(forms.ModelForm):      
    
       class Meta :
            model = Department
            fields = ('name','established')
            
       def __init__(self, *args , **kwargs):                         
              super(DepartmentForm,self).__init__(*args,**kwargs)              
              self.fields['name'].error_messages['required'] = "Please enter the name of the department"              
       
	
 
class DegreeForm(forms.ModelForm):      
    
       class Meta :
            model = Degree
            fields = ('name','established')
            
       def __init__(self, *args , **kwargs):                         
              super(DegreeForm,self).__init__(*args,**kwargs)              
              self.fields['name'].error_messages['required'] = "Please enter the name of the degree"              
       
	
        

class CourseForm(forms.ModelForm):
    
    class Meta :
       model = Course
       fields = ('name','introduced','departments')
       
    def __init__(self,*args,**kwargs):
       institute = None
       if 'institute' in kwargs.keys() :
              institute = kwargs['institute']
              kwargs.pop('institute')
              
       super(CourseForm,self).__init__(*args,**kwargs)
       self.fields['name'].error_messages['required'] = "Please enter the name of the Course"       
       self.fields['departments'].queryset = Department.objects.filter(institute__id=institute.id)
       
       
       


class LocationForm(forms.Form):
       country = forms.ModelChoiceField(queryset=None,empty_label=None)
       state = forms.CharField(max_length=200)
       city = forms.CharField(max_length=100,required=False,initial="")
       address = forms.CharField(max_length=3000,required=False,initial="")     
       latitude = forms.FloatField(widget=forms.HiddenInput())
       longitude = forms.FloatField(widget=forms.HiddenInput())
       
       
       def __init__(self, *args , **kwargs):              

              super(LocationForm,self).__init__(*args,**kwargs)            
              
              #increase the size of address field
              self.fields['address'].widget.attrs['size'] = 50
              self.fields['country'].widget.attrs['id'] =  "country2"
              self.fields['country'].queryset = Country.objects.all().order_by("name")
              self.fields['city'].widget.attrs['id'] = "city2"
              self.fields['state'].widget.attrs['id'] = "state2"
              #self.fields['state'].queryset = State.objects.all().order_by("-name")
              self.fields['address'].widget.attrs['id'] = "address2"
              self.fields['longitude'].widget.attrs['id'] = "longitude2"
              self.fields['latitude'].widget.attrs['id'] = "latitude2"               
              self.fields['longitude'].initial = 0              
              self.fields['latitude'].initial = 0
              
              
              #configure error messages for the location attributes
              self.fields['country'].error_messages['required'] = "You  should enter the country name"              
              self.fields['state'].error_messages['required'] = "You should enter the state name"
              
             
       
class FacultyProfessionalForm(forms.Form):
       subjects = forms.CharField(max_length=3000,widget=forms.Textarea)
       specialization = forms.CharField(max_length=255)
       designation = forms.CharField(max_length=100)
       website = forms.URLField(required=False)       
       
        
       def __init__(self, *args , **kwargs):
              super(FacultyProfessionalForm,self).__init__(*args,**kwargs)
              self.fields['designation'].error_messages['required'] = "You  should enter the  designation"
              self.fields['specialization'].error_messages['required'] = "You  should enter the specialization"             
              self.fields['subjects'].required = False
              

class StudentProfessionalForm(forms.ModelForm):
       website = forms.URLField(required=False)     
       class Meta :
            model = Student
            fields = ('whatiamdoing','company','title','industry','market')
            
            
       def __init__(self, *args , **kwargs):              
              super(StudentProfessionalForm,self).__init__(*args,**kwargs)            
              #intialize markets and industries
              self.fields['industry'] = IndustryChoiceField(queryset=None,required=False)
              self.fields['industry'].queryset = Industry.objects.all()
              self.fields['market'] = MarketChoiceField(queryset=None,required=False)
              self.fields['market'].queryset = Market.objects.all()         
             
              self.fields['whatiamdoing'].required = True
              self.fields['whatiamdoing'].initial = ""
              self.fields['whatiamdoing'].error_messages['required'] = "Please enter your professional details"
              
       
       def clean(self):
              ''' make sure what he selected matches fields he filled'''
              if 'whatiamdoing' not in self.cleaned_data :
                     return self.cleaned_data 
              
              if self.cleaned_data['whatiamdoing']:       
                     option = self.cleaned_data['whatiamdoing'].lower() 
                     if option == "employee" :
                          #All three must be filled
                          if len(self.cleaned_data['company'].strip()) <= 0:                     
                             self.errors['company'] = forms.util.ErrorList([u"Please enter company name"])
                          if len(self.cleaned_data['title'].strip()) <= 0:                       
                              self.errors['title'] = forms.util.ErrorList([u"Please enter the title you have at your office"])
                          if self.cleaned_data['industry'] is None  :
                              self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                          if self.cleaned_data['market'] is None  :
                              self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])    
                     elif option == "owner" :                     
                            if len(self.cleaned_data['company'].strip()) <= 0:                     
                                   self.errors['company'] = forms.util.ErrorList([u"Please enter company name"])
                            if self.cleaned_data['industry'] is None :
                                   self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                            if self.cleaned_data['market'] is None  :
                              self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])           
                     elif option == "lwork" or option == "freelance" :
                               if self.cleaned_data['industry'] is None :
                                   self.errors['industry'] = forms.util.ErrorList([u"Please enter the industry at which you are working"])
                               if self.cleaned_data['market'] is None  :
                                   self.errors['market'] = forms.util.ErrorList([u"Please enter the market "])
                     
              return self.cleaned_data              
              
              
            
       
              
              
              
              
              
                          
       
       
       
       
       
       
              
 
 
 
 
 
 
 
 
      
      
      
      
      
      
      
      
      
      
      
      
      
      
       
      
      
      
      
      
      
      
       
       
       
                  
                       
