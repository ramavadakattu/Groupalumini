import os
from django.db.models import signals
import settings
from whoosh import store, fields, index
from whoosh.filedb.filestore import FileStorage
from institution.models import StudentInstitute,FacultyInstitute



# Create your models here.
import logging
import logging.config



mlogger = logging.getLogger(__name__)


    
    
    
    
'''   
def adddoc(object,writer,created):
    mlogger.debug("adding index for %s " % (object.__class__.__name__))    
    
    if object.__class__.__name__ == "StudentInstitute" :
            si = object
            student = si.student
            institute = si.institute
            student = si.student
            name = student.profile.fullname        
            instituteid  = unicode(institute.id)
            id = unicode("student"+str(student.id)+str(institute.id))
            
            #fill the content
            content = student.profile.user.email+" "\
                      +student.profile.fullname+"  "
            
            if student.industry is not None :
                content = content + student.industry +"   "
                
            if si.coursename is not None :
                content = content + si.coursename+"  "
                
            if student.company is not None :
                content = content + student.company+"  "                
             
            if student.title is not None :
                content = content + student.title+"   "                
               
            if si.toyear is not None :
                content = content + unicode(si.toyear) +"   "
                
                
            mlogger.debug("content = %s " % (content,));
            mlogger.debug("institute id = %s" % (instituteid,))
            mlogger.debug("id = %s" %(id,))
            mlogger.debug("....................................")
            #import pdb
            #pdb.set_trace()
            if created :
                writer.add_document(name=name,content=content,instituteid=instituteid,id=id)               
            else :
                writer.update_document(name=name,content=content,instituteid=instituteid,id=id)                
    elif  object.__class__.__name__ == "FacultyInstitute" :
            fi = object
            faculty = fi.faculty
            institute = fi.institute
            faculty = fi.faculty
            name = faculty.profile.fullname
            instituteid = unicode(institute.id)
            id = unicode("faculty"+str(faculty.id)+str(institute.id))
            
            #fill the content
            content = faculty.profile.user.email+"  "\
                      +faculty.profile.fullname+"   "
                    
            
            if fi.specialization is not None :
                content = content + fi.specialization +"   "
                
            if fi.subjects is not None :
                content = content + fi.subjects + "   "                
            
            mlogger.debug("content = %s " % (content,));
            mlogger.debug("institute id = %s" % (instituteid,))
            mlogger.debug("....................................")
            mlogger.debug("id = %s" %(id,))
            #import pdb
            #pdb.set_trace
            if created :
                writer.add_document(name=name,content=content,instituteid=instituteid,id=id)                
            else :
                writer.update_document(name=name,content=content,instituteid=instituteid,id=id)
                
           
            
    '''
     

