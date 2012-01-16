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

#mainly this index on top of student and faculty
#name is the Student name
#content is the combination of content from several fields
#which institutes does this student belongs to
#id is of type Studentid and FacultyId

mlogger.debug("Setting up search..........................")

WHOOSH_SCHEMA = fields.Schema(name=fields.TEXT(stored=True),                              
                              content=fields.TEXT,
                              instituteid=fields.KEYWORD,
                              id=fields.ID(stored=True, unique=True))


def create_index(sender=None, **kwargs):
    mlogger.debug("setting up whoosh index.........................")  
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
     
    if index.exists_in(settings.WHOOSH_INDEX) :
        pass
    else :   
        ix = index.create_in(settings.WHOOSH_INDEX,WHOOSH_SCHEMA)
        build_clean_index()
        
        
signals.post_syncdb.connect(create_index)        
        

def build_clean_index():
    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = storage.open_index()
    writer = ix.writer()
    try:
        mlogger.debug("building index from scratch.....................")        
        mlogger.debug("adding objects...................")
        
        for si in StudentInstitute.objects.all():
             adddoc(si,writer,True)   
          
        for fi in FacultyInstitute.objects.all():
             adddoc(fi,writer,True)
    finally:            
        writer.commit()
        ix.close()



    
def adddoc(object,writer,created):
    mlogger.debug("adding index for %s " % (object.__class__.__name__))    
    
    if object.__class__.__name__ == "StudentInstitute" :
            si = object
            student = si.student
            institute = si.institute
            student = si.student
            name = student.profile.fullname        
            instituteid  = unicode(institute.id)
            id = unicode(str(institute.id)+"student"+str(student.id))
            
            mlogger.debug("what is the id = %s " % (id,))
            
            #fill the content
            content = " "\
                      +student.profile.fullname+"  "
            
            if student.industry is not None :
                content = content + student.industry.name +"   "
             
            if student.market is not None :
                content = content + student.market.name +"   "    
                
            if si.course.name is not None :
                content = content + si.course.name+"  "
                
            if si.department.name is not None :
                content = content + si.department.name+"  "                
                
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
            id = unicode(str(institute.id)+"faculty"+str(faculty.id))
            
            mlogger.debug("what is the id = %s " % (id,))
            
            #fill the content
            content = "  "\
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
                
           




def update_index(sender, instance, created, **kwargs):
    mlogger.debug("updating the index....................")
    ix2 = index.open_dir(settings.WHOOSH_INDEX)
    writer2 = ix2.writer()
    try:        
        if instance.__class__.__name__ == 'StudentInstitute' :
                si = instance        
                student = si.student            
                for i in student.institutes.all() :
                    si = StudentInstitute.objects.get(student__id = student.id,institute__id=i.id)
                    adddoc(si,writer2,created)
                    
        elif instance.__class__.__name__ == "FacultyInstitute" :
                fi = instance
                faculty = fi.faculty            
                for i in faculty.institutes.all() :
                    fi = FacultyInstitute.objects.get(faculty__id = faculty.id,institute__id=i.id)
                    adddoc(fi,writer2,created)
    finally:              
        writer2.commit()
        ix2.close()
    
    
       
 
#signals.post_save.connect(update_index, sender=StudentInstitute)
#signals.post_save.connect(update_index, sender=FacultyInstitute)               
    
   
