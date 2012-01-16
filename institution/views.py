from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404
from session_messages import create_message
from django.contrib.auth import authenticate ,login ,logout
import settings
import os
from django.template.loader import render_to_string
from django.contrib.auth.models import UserManager
from django.contrib.auth.views import redirect_to_login
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.utils import simplejson
from django.db.models import Q

import datetime
import logging
import logging.config


from institution.forms import LocationForm,IRegForm , LoginForm , FacultyForm , StudentForm , ImageUploadForm , ChangePasswordForm , ForgotPasswordForm , DepartmentForm , CourseForm , DegreeForm
from institution.forms import FacultyProfessionalForm,StudentProfessionalForm
from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , photo_file_path 
from institution.models import deliverEmail , Department , Course , Degree
from location.models import Country,State
from statistics.models import Industry,Market
import random, sha


from events.models import Event , EventAttendance
from jobs.models import Job
from askalumini.models import Question , Answer
from payments.models import Donation , Fund
from publish.models import Entry , Comment


mlogger = logging.getLogger(__name__)

# Create your views here.

def registerInstitution(request):
    ''' method which display and registration an institution'''
     #for now display the question
    mlogger.debug("Registering an institute................")    
    if request.method == 'GET':
        #display form
        form = IRegForm(0)            
    else:       
        form = IRegForm(0,request.POST,request.FILES)        
        if form.is_valid() :
            inst = form.save(commit=False)
            inst.admin = createAdmin(form.cleaned_data['adminemail'],form.cleaned_data['password1'],form.cleaned_data['adminname'])            
            inst.save()
            inst.admin.get_profile().institutes.add(inst)
            mlogger.debug("Creating an institution %s" %(inst.name,))
            #associate institute logo as avatar of admin            
            createAdminAvatar(request,inst.admin,'logo')
            fullactivationurl = inst.admin.get_profile().get_full_activation_url(inst)
            deliverEmail('newinstitute_subject.html','newinstitute_message.html',{'institute':inst,'fullactivationurl':fullactivationurl,'user':inst.admin,'password':form.cleaned_data['password1']},inst.admin.email)
            #Tell ALumclub admin about new registration
            emails = getALumClubAdminUrls()
            deliverEmail('tell_new_institute_registration.html','tell_new_institute_registration_message.html',{'institute':inst,'fullactivationurl':fullactivationurl,'user':inst.admin,'password':form.cleaned_data['password1']},emails)
            #redirect
            return HttpResponseRedirect("http://%s%s/"%(inst.subdomain,settings.DOMAIN_NAME))
        else :            
            pass

    return render_to_response("institution/register.html",{'form':form},RequestContext(request))  


def createAdminAvatar(request,user,fieldname):
    ''' associatess institute logo as admin avatar'''    
    path = photo_file_path(user.get_profile(),request.FILES[fieldname].name)
    profile = user.get_profile()
    mlogger.debug("creating admin avatar.................................")   
    new_file = profile.photo.save(path, request.FILES[fieldname])


def  createAdmin(email,password,name):
        ''' Create an admin from the given email and password'''
        mlogger.debug("Creating admin email = %s " %(email,))    
        u = User.objects.create_user(email.replace("@","_").replace(".","_"),email)
        u.set_password(password)
        u.save()        
        #he is admin save his profile
        up = UserProfile()
        up.country = Country.objects.all()[0]
        up.isadmin = True
        up.fullname = name
        up.user = u
        up.save()
        incorporateEmailActivation(up)
        return u
    
    
def  createMember(name,email,password,type,sform,institute):
        ''' Create an admin from the given email and password'''
        mlogger.debug("Creating admin email = %s " %(email,))
        u = User.objects.create_user(email.replace("@","_").replace(".","_"),email)
        u.set_password(password)        
        u.save()        
        #he is admin save his profile
        up = UserProfile()
        up.isadmin = False
        up.user = u
      
        
        if type.lower() == "student":
           up.isStudent = True
        else:
           up.isFaculty = True
           
        up.fullname = name       
        up.save()
        up.institutes.add(institute)
        incorporateEmailActivation(up)
        return up
    
def incorporateEmailActivation(up):
    ''' let us verify the user email '''
    salt = sha.new(str(random.random())).hexdigest()[:5]
    up.activation_key = sha.new(salt+up.fullname).hexdigest()
    up.save()
    
  
def displayHome(request):
    ''' displays the home page for a given institute or alumclub based   on subdomain name'''
    mlogger.debug("Institution %s" %(str(request.institute)))
  
    if request.institute is not None :
        #institute Home page
        institute = request.institute
        if request.method == "GET" :            
            if request.user.is_authenticated() :
                return HttpResponseRedirect(reverse('dashboardurl'))     
            else :
                form = LoginForm(request.institute)
                return render_to_response("institution/institute_home.html",{ 'form':form},RequestContext(request))                    
        else :
            form = LoginForm(request.institute,request.POST)            
            if form.is_valid() :
                #authenticate and login user
                u = authenticate(email=request.POST['email'],password=request.POST['password'])                
                login(request,u)                
                if 'rememberme' in request.POST.keys() :
                    #persistant session store the cookie for 10 weeks
                    request.session.set_expiry(70*24*60*60)
                else :
                    #browser length sessions
                    request.session.set_expiry(0)
                profile = u.get_profile()    
                logincount = profile.logincount
                if logincount is None or logincount == 0 :
                    profile.logincount = 1
                    profile.profilepercent = 33
                    profile.save()
                    
                    return HttpResponseRedirect(reverse('newlocationformurl'))
                    #return HttpResponseRedirect(reverse('newprofessionalformurl'))
                return HttpResponseRedirect(reverse('dashboardurl'))
            else :
                return render_to_response("institution/institute_home.html",{'form':form},RequestContext(request))            
    else:
        #Alumclub Home page
        return render_to_response("alumclub_home.html",{},RequestContext(request))
        
        
def registerMember(request):
    ''' register new member it may be student or faculty'''
    mlogger.debug("Institution %s" %(str(request.institute)))
    mlogger.debug("Registering a new member it can either student or Faculty")
    
    if request.institute is not None :
        if request.method == "GET" :        
            fform = FacultyForm(request.institute.id,False)
            sform = StudentForm(request.institute.id,False)            
            states = State.objects.all().order_by("id")
            industries = Industry.objects.all()
            return render_to_response("institution/newmember.html",{'industries':industries,'fform':fform,'sform':sform,'states':states,'form_default':'student'},RequestContext(request))
        elif request.method == "POST":
            if request.POST['whichform'] == "student" :
                whichform = "student"
                sform = StudentForm(request.institute.id,0,request.POST)
                fform = FacultyForm(request.institute.id,0)
                if sform.is_valid() :                    
                    #give him the success message
                    student = sform.save(commit=False)
                    up = createMember(sform.cleaned_data['name'],sform.cleaned_data['email'],sform.cleaned_data['password'],whichform,sform,request.institute)
                    student.profile = up              
                    student.save()              
                    #Student Institute                    
                    si = StudentInstitute()
                    si.institute = request.institute
                    si.student = student
                    si.fromyear = sform.cleaned_data['fromyear']                  
                    if len(sform.cleaned_data['toyear'].strip()) > 0 :
                        si.toyear = sform.cleaned_data['toyear']                  
                    si.course = sform.cleaned_data['course']
                    si.department = sform.cleaned_data['department']
                    si.degree = sform.cleaned_data['degree']                    
                    si.save()                   
                    #Create message
                    
                    fullactivationurl = student.profile.get_full_activation_url(request.institute)                    
                    deliverEmail('newstudent_subject.html','newstudent_message.html',{'fullactivationurl':fullactivationurl,'institute':request.institute,'user':up.user,'password':sform.cleaned_data['password']},up.user.email)
                    
                    # TEll alumclub admin and institute admin about regitration
                    emails = getALumClubAdminUrls()
                    emails.append(request.institute.admin.email)
                    deliverEmail('tell_new_alumini_registration.html','tell_new_alumini_registration_message.html',{'fullactivationurl':fullactivationurl,'institute':request.institute,'user':up.user,'password':sform.cleaned_data['password']},emails)
                    #Tell institute admin about new registration                    
                    
                    create_message(request,"Successfully Registered.Your will be able to login once your account is  verified by the Insitute admin.")
                    return HttpResponseRedirect("/")                       
                else :
                    return render_to_response("institution/newmember.html",{'fform':fform,'sform':sform,'form_default':whichform},RequestContext(request))                        
            elif request.POST['whichform'] == "faculty" :
                whichform = "faculty"           
                sform = StudentForm(request.institute.id,0)
                fform = FacultyForm(request.institute.id,0,request.POST)
                if fform.is_valid() :
                    #give him the success message
                    faculty = fform.save(commit=False)
                    up = createMember(fform.cleaned_data['name'],fform.cleaned_data['email'],fform.cleaned_data['password'],whichform,fform,request.institute)
                    faculty.profile = up
                    faculty.save()                    
                    #save faculty institute relationship
                    fi = FacultyInstitute()
                    fi.institute = request.institute
                    fi.faculty = faculty                
                    fi.department = fform.cleaned_data['department']
                    fi.save()
                    #Create message
                    
                    fullactivationurl = faculty.profile.get_full_activation_url(request.institute)                    
                    deliverEmail('newfaculty_subject.html','newfaculty_message.html',{'fullactivationurl':fullactivationurl,'institute':request.institute,'user':up.user,'password':fform.cleaned_data['password']},up.user.email)
                    
                    # TEll alumclub admin and institute admin about regitration
                    emails = getALumClubAdminUrls()
                    emails.append(request.institute.admin.email)
                    deliverEmail('tell_new_alumini_registration.html','tell_new_alumini_registration_message.html',{'fullactivationurl':fullactivationurl,'institute':request.institute,'user':up.user,'password':fform.cleaned_data['password']},emails)
                    
                    create_message(request,"Successfully Registered.Your will be able to login once your account is  verified by the Insitute admin.")
                    
                    #Redirect to institute home
                    return HttpResponseRedirect("/")                          
                    
                else :
                    return render_to_response("institution/newmember.html",{'fform':fform,'sform':sform,'form_default':whichform},RequestContext(request))                        
  
    
            
@login_required(redirect_field_name='next')
def viewDashboard(request):
    ''' present the user with the institute dashboard '''    
    if request.institute is not None :              
        #get latest three events
        events = Event.objects.filter(institute__id=request.institute.id).order_by('-createddate')[:3]
        events = list(events)
        #get latest three jobs
        jobs = Job.objects.filter( Q(institute__isnull=True) | Q(institute__id=request.institute.id)  ).order_by('-createddate')[:3]
        jobs = list(jobs)        
        #get latest three discussions
        questions = Question.objects.filter(institute__id=request.institute.id).order_by('-createddate')[:3]
        questions = list(questions)      
        #get latest three donations
        donations = Donation.objects.filter(institute__id=request.institute.id).order_by('-createddate')[:3]
        donations = list(donations)
        #get latest three newsletters
        entries = Entry.objects.filter(institute__id=request.institute.id,research_paper=False).order_by('-createddate')[:3]
        entries = list(entries)
        #get latest three answers
        answers = Answer.objects.filter(question__institute__id=request.institute.id).order_by('-createddate')[:2]
        answers = list(answers)        
        #get latest three created donations
        funds = Fund.objects.filter(institute__id=request.institute.id).order_by('-createddate')[:3]
        funds = list(funds)       
        #get the lastest three comments
        comments = Comment.objects.filter(entry__institute__id=request.institute.id).order_by('-createddate')[:3]
        comments = list(comments)
        
        #get people attending the events
        eventattendance = EventAttendance.objects.filter(institute__id=request.institute.id).order_by('-createddate')[:3]
        eventattendance = list(eventattendance)
        
        
        
        #sort all the stuff based createddate
        latest_entries = []
        if events :
            latest_entries = latest_entries+events
        if jobs :    
            latest_entries =  latest_entries+jobs
        if questions:    
            latest_entries  = latest_entries+questions
        if donations:    
            latest_entries = latest_entries+donations
        if entries :     
            latest_entries = latest_entries+entries
        if answers  :     
            latest_entries = latest_entries+answers 
        if funds :     
            latest_entries = latest_entries+funds
        if comments :     
            latest_entries = latest_entries+comments
        if eventattendance :
            latest_entries = latest_entries+eventattendance
            
            
        #display them on the dashboard
        latest_entries.sort(lambda x, y: cmp(x.createddate,y.createddate),reverse=True)
        
        nlatest_entries = []
        for entry in latest_entries[:10] :
                nlatest_entries.append((entry.__class__.__name__,entry))
        
       
                
        return render_to_response("institution/dashboard.html",{'latest_entries':nlatest_entries},RequestContext(request))
    
    
@login_required(redirect_field_name='next')    
def editProfile(request):
    mlogger.debug("Editing the profile of a member")   
    user = request.user   
    whichform = None
    profile = user.get_profile()   
    if request.method == "GET" :       
        if profile.isFaculty  :
                    whichform = "faculty"
                    #intialize the form
                    f = Faculty.objects.get(profile__id = profile.id )
                    fi = FacultyInstitute.objects.get(faculty__id = f.id,institute__id = request.institute.id)
                    initial_data = {'institutename':request.institute.name,
                                   'name':profile.fullname,
                                   'email':user.email,                               
                                    'department':fi.department.id}                   
                    fform = FacultyForm(request.institute.id,request.user.id ,initial=initial_data,instance=f)
                    industries = Industry.objects.all()
                    return render_to_response("institution/editprofile.html",{'industries':industries,'fform':fform,'whichform':whichform},RequestContext(request))
        elif user.get_profile().isStudent :                    
                    whichform = "student"
                    s = Student.objects.get(profile__id = profile.id )
                    si = StudentInstitute.objects.get(student__id = s.id,institute__id=request.institute.id)
                    initial_data = {'institutename':request.institute.name,
                                   'name':profile.fullname,
                                   'email':user.email,
                                    'website':profile.personalsite,
                                    'fromyear':si.fromyear,
                                   'toyear':si.toyear,
                                   'course':si.course.id,
                                   'department':si.department.id,
                                   'degree':si.degree.id}                    
                    sform = StudentForm(request.institute.id,request.user.id,initial=initial_data,instance=s)
                    industries = Industry.objects.all()
                    return render_to_response("institution/editprofile.html",{'industries':industries,'sform':sform,'whichform':whichform},RequestContext(request))
    elif request.method == "POST":
        if profile.isFaculty  :
            whichform = "faculty"
            f = Faculty.objects.get(profile__id = profile.id )
            fi = FacultyInstitute.objects.get(faculty__id = f.id,institute__id = request.institute.id)
            
            #update the user data
            fform = FacultyForm(request.institute.id,request.user.id,request.POST)
            if fform.is_valid() :
                profile.user.email = fform.cleaned_data['email']
                profile.user.username =  fform.cleaned_data['email'].replace("@","_").replace(".","_")
                profile.user.save()
                profile.fullname = fform.cleaned_data['name']
                            
                profile.save()               
                fi.department = fform.cleaned_data['department']
                fi.save()
                #Create message
                create_message(request,"Successfully update your profile..............")
                #Redirect to institute home
                return HttpResponseRedirect(reverse('editprofileurl'))
            else :
                return render_to_response("institution/editprofile.html",{'fform':fform,'whichform':whichform},RequestContext(request)) 
        elif profile.isStudent :
            whichform = "student"
            s = Student.objects.get(profile__id = profile.id )
            si = StudentInstitute.objects.get(student__id = s.id,institute__id=request.institute.id)
            
            #update the student data
            sform = StudentForm(request.institute.id,request.user.id,request.POST)
            if sform.is_valid() :
                profile.user.email = sform.cleaned_data['email']
                profile.user.username =  sform.cleaned_data['email'].replace("@","_").replace(".","_")
                profile.user.save()
                profile.fullname = sform.cleaned_data['name']                 
                profile.save()               
                si.toyear = sform.cleaned_data['toyear']
                si.fromyear = sform.cleaned_data['fromyear']                
                si.department = sform.cleaned_data['department']
                si.course = sform.cleaned_data['course']
                si.degree = sform.cleaned_data['degree']
                si.save()               
                #Create message
                create_message(request,"Successfully update your profile..............")
                #Redirect to institute home
                return HttpResponseRedirect(reverse('editprofileurl'))                         
            else :
                return render_to_response("institution/editprofile.html",{'sform':sform,'whichform':whichform},RequestContext(request))
    

@login_required(redirect_field_name='next')    
def changePassword(request):
    mlogger.debug("Changing the password.........................")
    if request.method == "GET" :
       form = ChangePasswordForm(request.user.id)
    elif request.method == "POST" :        
        form = ChangePasswordForm(request.user.id,request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            create_message(request,"Sucessfully changed your password..............")
            return HttpResponseRedirect(reverse('changepasswordurl'))
   
    return render_to_response("institution/changepassword.html",{'form':form},RequestContext(request))                        


@login_required(redirect_field_name='next')
def changePicture(request):   
    mlogger.debug("Changing the picture of the user...............")
    if request.method == "GET" :        
        form = ImageUploadForm()
        return render_to_response("institution/changephoto.html",{'form':form},RequestContext(request))                        
    elif request.method == "POST" :         
         form = ImageUploadForm(request.POST,request.FILES)
         if form.is_valid() :            
            createAdminAvatar(request,request.user,'newphoto')
            create_message(request,"Successfully uploaded the new photo.............")
            return HttpResponseRedirect(reverse('changepictureurl'))
            
         return render_to_response("institution/changephoto.html",{'form':form},RequestContext(request))                        
    
    
    
def memeberlogout(request):
    mlogger.debug("Logging out ...................")   
    logout(request)
    create_message(request,"Successfully logged out ................")
    return HttpResponseRedirect(reverse('indexurl'))
    

@login_required(redirect_field_name='next')    
def editInstitute(request):
    mlogger.debug("Editing the institute data")
    
    if request.method == "GET" :
        admin = request.institute.admin
        profile = admin.get_profile()
        initial_data = {'adminname':profile.fullname,
                                           'adminemail':admin.email,
                                            }    
        form = IRegForm(request.institute.id,initial=initial_data,instance=request.institute)
    elif request.method == "POST" :
        admin = request.institute.admin
        profile = admin.get_profile()        
        form = IRegForm(request.institute.id,request.POST,instance=request.institute)
        
        if form.is_valid() :
            create_message(request,"Update the institute settings successfully ................")
            profile.fullname = form.cleaned_data['adminname']
            profile.user.username = form.cleaned_data['adminemail'].replace("@","_").replace(".","_")
            profile.save()
            admin.email = form.cleaned_data['adminemail']
            admin.save()
            inst = form.save(commit=False)
            inst.save()
            
    return render_to_response("institution/editinstitute.html",{'form':form},RequestContext(request))
    
    

    
        
        
def forgotPassword(request) :   
    mlogger.debug("resetting password")
    if request.method == 'GET' :
        form =  ForgotPasswordForm()
        return render_to_response("institution/forgotpassword.html",{'form':form},RequestContext(request))
    elif request.method == 'POST' :
        form = ForgotPasswordForm(request.POST)
        if form.is_valid() :            
            user = User.objects.get(email=form.cleaned_data['email'])
            #generate new password
            newpassword = UserManager().make_random_password()
            user.set_password(newpassword)
            user.save()
            subject = render_to_string('institution/emails/forgotpassword_subject.html',{'institute':request.institute,'fuser':user}, RequestContext(request))
            message = render_to_string('institution/emails/forgotpassword_message.html',{'institute':request.institute,'password':newpassword,'fuser':user} ,RequestContext(request))            
            mlogger.debug("Subject = %s message = %s " % (subject,message))
            msg = EmailMessage(subject,message, settings.EMAIL_HOST_USER, [user.email])
            msg.content_subtype = "html"
            msg.send(fail_silently=True)       
            create_message(request,"Successfully resetted the password and sent it to your mail")
            return redirect_to_login(next='')                  
        else :
            return render_to_response("institution/forgotpassword.html",{'form':form},RequestContext(request))   


@login_required(redirect_field_name='next') 
def approveMemebers(request):
    mlogger.debug('admin approving %s .............')
    if request.method == "GET" :
        if not  request.user.get_profile().isadmin :
             create_message(request,"Your are not authorized to do this operation............")
             return HttpResponseRedirect(reverse('dashboardurl'))
        
       
        paginator =  Paginator(Faculty.objects.filter(institutes__in=[request.institute.id],profile__approved=0).order_by('-createddate'),1)
        toapprove = paginator.page(1)
        if toapprove.object_list :
            fi = FacultyInstitute.objects.get(faculty__id = toapprove.object_list[0].id,institute__id = request.institute.id)
            return render_to_response("institution/approve_member.html",{'institute':request.institute,'toapprove':toapprove.object_list[0],'entity':'faculty','fi':fi},RequestContext(request))
        else :            
            si = None
            paginator = Paginator(Student.objects.filter(institutes__in=[request.institute.id],profile__approved=0).order_by('-createddate'),1)
            toapprove = paginator.page(1)
            
            if toapprove.object_list :                
                toapprove = toapprove.object_list[0]
                si = StudentInstitute.objects.get(student__id = toapprove.id,institute__id=request.institute.id)
            else :
                toapprove = None
            return render_to_response("institution/approve_member.html",{'toapprove':toapprove,'entity':'student','si':si},RequestContext(request))
    elif request.method == "POST":
         d = {}
         id = int(request.POST['id'])
         entity = request.POST['entity']
         flag = int(request.POST['flag'])
         
         k = None
        
         if entity == "student":
            k = Student.objects.get(pk=id)            
         else :
            k = Faculty.objects.get(pk=id)
        
         profile = k.profile
         #approve
         if flag :
            profile.approved = 1
            d['message'] = "Sucessfully approved..........."
         #Reject the member ship
         else:
             profile.approved = -1
             d['message'] = "Successfully rejected .................."
         
         profile.save()
         #deliver mail
         if entity =="student":
            deliverEmail('studentapproved_subject.html','studentapproved_message.html',{'user':request.user,'approved':profile.approved},profile.user.email)
         else :
            deliverEmail('facultyapproved_subject.html','facultyapproved_message.html',{'user':request.user,'approved':profile.approved},profile.user.email)
            
         
         d['success'] = "yes"      
         json = simplejson.dumps(d)         
         return HttpResponse(json)    

    
         
         
@login_required(redirect_field_name='next')     
def displayApproveHome(request):
    mlogger.debug("displaying the approval home")
    if not  request.user.get_profile().isadmin :
         create_message(request,"Your are not authorized to do this operation............")
         return HttpResponseRedirect(reverse('dashboardurl'))          
    return render_to_response("institution/approve.html",{},RequestContext(request))
    
    
    
@login_required(redirect_field_name='next')         
def showDepartments(request):
    mlogger.debug("show all the departments..................")
    departments = Department.objects.filter(institute__id=request.institute.id)
    return render_to_response("institution/department/departments.html",{'departments':departments},RequestContext(request))
    
    
    
     
@login_required(redirect_field_name='next')         
def addDepartment(request):    
    if request.method == "GET":
        form = DepartmentForm()
        return render_to_response("institution/department/add_department.html",{'form':form},RequestContext(request))
    elif request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid() :
            d = Department()
            d.name = form.cleaned_data['name']
            d.established = form.cleaned_data['established']
            d.institute = request.institute
            d.user = request.user
            d.save()
            create_message(request,"Succesfully added the department")
            return HttpResponseRedirect(reverse('showdepartmenturl'))
        else:
            return render_to_response("institution/department/add_department.html",{'form':form},RequestContext(request))
            
@login_required(redirect_field_name='next')            
def showCourses(request):
    mlogger.debug("show all the courses under each department..................")
    departments = Department.objects.filter(institute__id=request.institute.id)
    return render_to_response("institution/courses/courses.html",{'departments':departments},RequestContext(request))
    


def addCourse(request):
    mlogger.debug("show all courses in all the departments...........")
    if request.method == "GET":
        form = CourseForm(institute=request.institute)
        return render_to_response("institution/courses/add_course.html",{'form':form},RequestContext(request))
    elif request.method == "POST" :
        form = CourseForm(request.POST,institute=request.institute)
        if form.is_valid():
            c = Course()
            c.name = form.cleaned_data['name']
            c.introduced = form.cleaned_data['introduced']
            c.user = request.user
            c.institute = request.institute
            c.save()
            c.departments = form.cleaned_data['departments']
            create_message(request,"Succesfully added the course")
            return HttpResponseRedirect(reverse('showcoursesurl'))           
        else:
            return render_to_response("institution/courses/add_course.html",{'form':form},RequestContext(request))
            
        
    
@login_required(redirect_field_name='next')        
def editDepartment(request,department_id):
    mlogger.debug("Editing the department  %s ", (department_id,))
    department_id = int(department_id)
    department = Department.objects.get(pk=department_id)
    if request.user.id == department.user.id :
        if request.method == "GET" :
                mlogger.debug("the person who posted the job is editing")
                form = DepartmentForm(instance=department)            
                return render_to_response('institution/department/add_department.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
                form = DepartmentForm(request.POST, instance=department)
                if form.is_valid() :
                    form.save()
                    create_message(request,"Successfuly  edited the department")
                    return HttpResponseRedirect(reverse('showdepartmenturl'))
                else:
                    return render_to_response('institution/department/add_department.html',{'form':form,'editmode':True},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this job")
        return HttpResponseRedirect(reverse('showdepartmenturl'))
        


    
@login_required(redirect_field_name='next')        
def deleteDepartment(request,department_id):
    mlogger.debug("Deleting the department  %s ", (department_id,))
    Department.objects.get(pk=int(department_id)).delete()
    create_message(request,"Successfuly deleted the department")
    return HttpResponseRedirect(reverse('showdepartmenturl'))


@login_required(redirect_field_name='next')            
def editCourse(request,course_id):
    mlogger.debug("Editing the Course  %s ", (course_id,))
    course_id = int(course_id)
    course = Course.objects.get(pk=course_id)
    if request.user.id == course.user.id :
        if request.method == "GET" :
                mlogger.debug("the person who posted the Course is editing")
                form = CourseForm(instance=course,institute=request.institute)            
                return render_to_response("institution/courses/add_course.html",{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
                form = CourseForm(request.POST, instance=course,institute=request.institute)
                if form.is_valid() :
                    form.save()
                    create_message(request,"Successfuly  edited the Course")
                    return HttpResponseRedirect(reverse('showcoursesurl'))
                else:
                    return render_to_response("institution/courses/add_course.html",{'form':form,'editmode':True},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this job")
        return HttpResponseRedirect(reverse('showcoursesurl'))
        
    


@login_required(redirect_field_name='next')                    
def deleteCourse(request,course_id):
    mlogger.debug("Deleting the Course  %s ", (course_id,))
    Course.objects.get(pk=int(course_id)).delete()
    create_message(request,"Successfuly deleted the course")
    return HttpResponseRedirect(reverse('showcoursesurl'))
    
    

def getMatchedStates(request):    
    mlogger.debug("Get the state look up results............")
    results = []   
    if request.method == "GET":
        if 'q' in request.GET.keys():
            value = request.GET['q']
            # Ignore queries shorter than length 3
            if len(value) > 0:
                model_results = State.objects.filter(name__istartswith=value)
                results = [ x.name for x in model_results ]
    json = simplejson.dumps(results)   
    return HttpResponse(json, mimetype='application/json')
    
    
def changeLocation(request):
        profile = request.user.get_profile()
        if request.method == "GET" :           
                initial_data = {'country':profile.country.id,
                                           'state':profile.state,
                                           'city':profile.city,
                                           'address':profile.address,
                                           'latitude':profile.latitude,
                                           'longitude':profile.longitude
                                          }                   
                form = LocationForm(initial=initial_data)
                return render_to_response("institution/changelocation.html",{'form':form},RequestContext(request))
        elif request.method == "POST" :
            form = LocationForm(request.POST)
            if form.is_valid() :            
                up = profile
                up.country =  form.cleaned_data['country']
                up.state = None if len(form.cleaned_data['state'].strip())  <= 0  else  form.cleaned_data['state'].strip()
                up.city = None if len(form.cleaned_data['city'].strip())  <= 0  else  form.cleaned_data['city'].strip() 
                up.address = None if len(form.cleaned_data['address'].strip())  <= 0  else  form.cleaned_data['address'].strip()  
                up.latitude = float(form.cleaned_data['latitude'])
                up.longitude = float(form.cleaned_data['longitude'])
                up.save()
                create_message(request,"Successfully changed to new location")
                return HttpResponseRedirect(reverse('changelocationurl'))     
            else:
                return render_to_response("institution/changelocation.html",{'form':form},RequestContext(request))
                
    
   

def addDegree(request):
    if request.method == "GET":
        form = DegreeForm()
        return render_to_response("institution/degrees/add_degree.html",{'form':form},RequestContext(request))
    elif request.method == "POST":
        form = DegreeForm(request.POST)
        if form.is_valid() :
            d = Degree()
            d.name = form.cleaned_data['name']
            d.established = form.cleaned_data['established']
            d.institute = request.institute
            d.user = request.user
            d.save()
            create_message(request,"Succesfully added the degree")
            return HttpResponseRedirect(reverse('showdegreeurl'))
        else:
            return render_to_response("institution/degrees/add_degree.html",{'form':form},RequestContext(request))
            


def showDegrees(request):
    mlogger.debug("show all the departments..................")
    degrees = Degree.objects.filter(institute__id=request.institute.id)
    return render_to_response("institution/degrees/degrees.html",{'degrees':degrees},RequestContext(request))
    
    

def editDegree(request,degree_id):
    mlogger.debug("Editing the department  %s ", (degree_id,))
    degree_id = int(degree_id)
    degree = Degree.objects.get(pk=degree_id)
    if request.user.id == degree .user.id :
        if request.method == "GET" :
                mlogger.debug("the person who posted the degreeis editing")
                form = DegreeForm(instance=degree)            
                return render_to_response('institution/degrees/add_degree.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
                form = DegreeForm(request.POST, instance=degree)
                if form.is_valid() :
                    form.save()
                    create_message(request,"Successfuly  edited the degree")
                    return HttpResponseRedirect(reverse('showdegreeurl'))
                else:
                    return render_to_response('institution/degrees/add_degree.html',{'form':form,'editmode':True},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this degree")
        return HttpResponseRedirect(reverse('showdegreeurl'))
        



def deleteDegree(request,degree_id):
    mlogger.debug("Deleting the Degree  %s ", (degree_id,))
    Degree.objects.get(pk=int(degree_id)).delete()
    create_message(request,"Successfuly deleted the degree")
    return HttpResponseRedirect(reverse('showdegreeurl'))
    
    
    
def activateEmail(request,userid,activation_key):
    mlogger.debug("Activating email.........................")    
    error = ''
    
    try :
          u =  User.objects.get(pk=userid)
          profile = u.get_profile()
                    
          if len(profile.activation_key) > 0 :
            if profile.activation_key == activation_key :                
                #logic for activation key expiration
                todaydate = datetime.datetime.now()
                if profile.createddate <   todaydate - datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS) :
                    #activation key has been expired
                    create_message(request,"Activation key has been expired.Please request for a new one")
                    return render_to_response("institution/activation_error.html",RequestContext(request))
                 
                #activate the user    
                profile.emailverified = True
                #reset the activation key
                profile.activation_key = ''
                profile.save()
                create_message(request,"Successfully activated your email")
                #either login or directly transfer him to the corresponding page
                return redirect_to_login(next='')
            else :                
                create_message(request,"Invalid activation key")         
          else :
            create_message(request,"Invalid Userid and activation key combination...............")
                
            return redirect_to_login(next='')
          return render_to_response("institution/activation_error.html",RequestContext(request))              
    except User.DoesNotExist :            
            create_message(request,"Invalid Userid and activation key combination...............")
            return render_to_response("institution/activation_error.html",RequestContext(request))
        
    


def getALumClubAdminUrls():
    emails = []
    for admin in settings.ADMINS :
        emails.append(admin[1])
    return emails

@login_required(redirect_field_name='next') 
def newLocationForm(request):       
        profile = request.user.get_profile()
        if request.method == "GET" :           
                form = LocationForm()
                return render_to_response("institution/locationform.html",{'form':form},RequestContext(request))
        elif request.method == "POST" :
            form = LocationForm(request.POST)
            if form.is_valid() :            
                up = profile
                up.country =  form.cleaned_data['country']
                up.state = None if len(form.cleaned_data['state'].strip())  <= 0  else  form.cleaned_data['state'].strip()
                up.city = None if len(form.cleaned_data['city'].strip())  <= 0  else  form.cleaned_data['city'].strip() 
                up.address = None if len(form.cleaned_data['address'].strip())  <= 0  else  form.cleaned_data['address'].strip()
                if (int(form.cleaned_data['latitude']) != 0):
                        up.latitude = float(form.cleaned_data['latitude'])
                if (int(form.cleaned_data['longitude']) != 0):        
                    up.longitude = float(form.cleaned_data['longitude'])
                up.save()
                create_message(request,"Added your location")                
                return HttpResponseRedirect(reverse('newprofessionalformurl'))     
            else:
                return render_to_response("institution/locationform.html",{'form':form},RequestContext(request))
                
                
@login_required(redirect_field_name='next')                 
def newProfessionalForm(request):      
    editmode = False
    if 'edit' in request.GET.keys() :
        editmode = True         
   
    profile = request.user.get_profile()
    
    if profile.isStudent :
        industries = Industry.objects.all()
        student = profile.student_set.all()[0]            
        if request.method == "GET":
            if editmode is False :
                form = StudentProfessionalForm()
            else :
                initial_data = {'website':profile.personalsite}               
                form = StudentProfessionalForm(initial=initial_data,instance=student)
            return render_to_response("institution/student_professional_form.html",{'editmode':editmode,'industries':industries,'form':form},RequestContext(request))
        elif request.method == "POST" :           
            form = StudentProfessionalForm(request.POST,instance=student)
            if form.is_valid() :                
                form.save()
                profile.website = form.cleaned_data['website']
                profile.save()
                
                if editmode :
                    create_message(request,"Updated your professional details")
                    return HttpResponseRedirect(reverse('newprofessionalformurl')+"?edit=1")
                else :    
                    create_message(request,"Successfully added your professional details")
                    return HttpResponseRedirect(reverse('dashboardurl'))
            else:
                return render_to_response("institution/student_professional_form.html",{'editmode':editmode,'industries':industries,'form':form},RequestContext(request))            
    elif profile.isFaculty :
        faculty = profile.faculty_set.all()[0]
        fi = FacultyInstitute.objects.get(faculty__id = faculty.id,institute__id = request.institute.id)
        
        if request.method == "GET":
            
            if editmode is False :
                    form = FacultyProfessionalForm()
            else :
                initial_data = {'subjects': fi.subjects,
                                'specialization':fi.specialization,
                                'designation':fi.designation
                                }               
                form = FacultyProfessionalForm(initial=initial_data)                   
            return render_to_response("institution/faculty_professional_form.html",{'editmode':editmode,'form':form},RequestContext(request))            
        elif request.method == "POST":
           
            form = FacultyProfessionalForm(request.POST)
            if form.is_valid() :            
                profile.website = form.cleaned_data['website']
                profile.save()
                
               
                fi.subjects = form.cleaned_data['subjects']
                fi.specialization = form.cleaned_data['specialization']
                fi.designation = form.cleaned_data['designation']
                fi.save()                
                
                if editmode :
                    create_message(request,"Updated your professional details")
                    return HttpResponseRedirect(reverse('newprofessionalformurl')+"?edit=1")                    
                else :    
                    create_message(request,"Successfully added your professional details")
                    return HttpResponseRedirect(reverse('dashboardurl'))
            else:
                return render_to_response("institution/faculty_professional_form.html",{'editmode':editmode,'form':form},RequestContext(request))
    elif profile.isadmin :
              return HttpResponseRedirect(reverse('dashboardurl'))
           
                