
from django import template
from django.template import Library, Node ,TemplateSyntaxError ,Variable
from institution.models import StudentInstitute,FacultyInstitute

register = Library()


class ShortProfileNode(Node):
    
    def __init__(self,institute,entity):
         self.institute = Variable(institute)
         self.entity = Variable(entity)
         
    
    
    def render(self,context):
        
        try :            
            tinstitute = self.institute.resolve(context)
            tentity = self.entity.resolve(context)                       
            if tentity.__class__.__name__ == "Student" :
                 return self.getStudentShortProfile(tinstitute,tentity)                
            elif tentity.__class__.__name__ == "Faculty":
                 return self.getFacultyShortProfile(tinstitute,tentity)
            elif tentity.__class__.__name__ == "UserProfile":
                 return self.getUserPShortProfile(tinstitute,tentity)
            elif tentity.__class__.__name__ == "User":
                 return self.getUserShortProfile(tinstitute,tentity)         
        except template.VariableDoesNotExist :
            return ''
        
    def getStudentShortProfile(self,institute,student):
        si = StudentInstitute.objects.get(student__id=student.id,institute__id=institute.id)
        return si.getSimpleProfile()        
        
        
    def getFacultyShortProfile(self,institute,faculty):        
        fi = FacultyInstitute.objects.get(faculty__id=faculty.id,institute__id=institute.id)
        return fi.getSimpleProfile()
        
        
    def getUserPShortProfile(self,institute,profile):
        if profile.isadmin  :
                    return "institute admin"
        elif profile.isStudent :
                student = profile.student_set.all()[0]
                return self.getStudentShortProfile(institute,student)
        elif profile.isFaculty :
                faculty = profile.faculty_set.all()[0]
                return self.getFacultyShortProfile(institute,faculty)
            
 
    def getUserShortProfile(self,institute,user):        
        return self.getUserPShortProfile(institute,user.get_profile())
      
   

def get_short_profile(parse,token):
    bits = token.split_contents()
    if len(bits) != 3 :
        raise TemplateSyntaxError, "% s tag takes exactly two arguments" % (bits[0],)
    
    return ShortProfileNode(bits[1],bits[2])



register.tag('get_short_profile',get_short_profile)
  

    