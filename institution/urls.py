from django.conf.urls.defaults import *


urlpatterns = patterns('institution.views',
        url(r'^$','displayHome',name='indexurl'),                               
        url(r'^register/$','registerInstitution',name='iregister'),
        url(r'^statelookup/$','getMatchedStates',name="statelookupurl"),
        url(r'^locationform/$','newLocationForm',name="newlocationformurl"),
        url(r'^professionalform/$','newProfessionalForm',name="newprofessionalformurl"),
        url(r'^newmember/$','registerMember',name='newmemberurl'),       
        url(r'^dashboard/$','viewDashboard',name="dashboardurl"),
        url(r'^editinstitute/$','editInstitute',name="editinstituteurl"),
        url(r'^member/editprofile/$','editProfile',name="editprofileurl"),
        url(r'^member/changepassword/$','changePassword',name="changepasswordurl"),
        url(r'^member/forgotpassword/$','forgotPassword',name="forgotpasswordurl"),
        url(r'^member/changelocation/$','changeLocation',name="changelocationurl"),
        url(r'^member/changepicture/$','changePicture',name="changepictureurl"),
        url(r'^member/logout/$','memeberlogout',name="logouturl"),        
        url(r'^member/activate/(?P<userid>\d+)/(?P<activation_key>\w+)/$','activateEmail',name='activationurl'),
        url(r'^approvemembers/$','approveMemebers',name="approvememberurl"),
        url(r'^departments/$','showDepartments',name="showdepartmenturl"),
        url(r'^adddepartment/$','addDepartment',name="adddepartmenturl"),
        url(r'^editdepartment/(?P<department_id>[0-9]+)/$','editDepartment',name="editdepartmenturl"),
        url(r'^deletedepartment/(?P<department_id>[0-9]+)/$','deleteDepartment',name="deletedepartmenturl"),
        url(r'^courses/$','showCourses',name="showcoursesurl"),
        url(r'^addcourse/$','addCourse',name="addcourseurl"),
        url(r'^editcourse/(?P<course_id>[0-9]+)/$','editCourse',name="editcourseurl"),
        url(r'^deletecourse/(?P<course_id>[0-9]+)/$','deleteCourse',name="deletecourseurl"),
         url(r'^degrees/$','showDegrees',name="showdegreeurl"),
        url(r'^adddegree/$','addDegree',name="adddegreeurl"),
        url(r'^editdegree/(?P<degree_id>[0-9]+)/$','editDegree',name="editdegreeurl"),
        url(r'^deletedegree/(?P<degree_id>[0-9]+)/$','deleteDegree',name="deletedegreeurl"),
        
       
       )