
from south.db import db
from django.db import models
from institution.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'FacultyInstitute'
        db.create_table('institution_facultyinstitute', (
            ('id', orm['institution.FacultyInstitute:id']),
            ('faculty', orm['institution.FacultyInstitute:faculty']),
            ('institute', orm['institution.FacultyInstitute:institute']),
            ('joineddate', orm['institution.FacultyInstitute:joineddate']),
            ('lastupdate', orm['institution.FacultyInstitute:lastupdate']),
            ('subjects', orm['institution.FacultyInstitute:subjects']),
            ('specialization', orm['institution.FacultyInstitute:specialization']),
            ('designation', orm['institution.FacultyInstitute:designation']),
            ('department', orm['institution.FacultyInstitute:department']),
        ))
        db.send_create_signal('institution', ['FacultyInstitute'])
        
        # Adding model 'StudentInstitute'
        db.create_table('institution_studentinstitute', (
            ('id', orm['institution.StudentInstitute:id']),
            ('student', orm['institution.StudentInstitute:student']),
            ('institute', orm['institution.StudentInstitute:institute']),
            ('joineddate', orm['institution.StudentInstitute:joineddate']),
            ('lastupdate', orm['institution.StudentInstitute:lastupdate']),
            ('fromyear', orm['institution.StudentInstitute:fromyear']),
            ('toyear', orm['institution.StudentInstitute:toyear']),
            ('course', orm['institution.StudentInstitute:course']),
            ('department', orm['institution.StudentInstitute:department']),
            ('degree', orm['institution.StudentInstitute:degree']),
        ))
        db.send_create_signal('institution', ['StudentInstitute'])
        
        # Adding model 'Degree'
        db.create_table('institution_degree', (
            ('id', orm['institution.Degree:id']),
            ('name', orm['institution.Degree:name']),
            ('established', orm['institution.Degree:established']),
            ('institute', orm['institution.Degree:institute']),
            ('createddate', orm['institution.Degree:createddate']),
            ('updateddate', orm['institution.Degree:updateddate']),
            ('user', orm['institution.Degree:user']),
        ))
        db.send_create_signal('institution', ['Degree'])
        
        # Adding model 'Faculty'
        db.create_table('institution_faculty', (
            ('id', orm['institution.Faculty:id']),
            ('profile', orm['institution.Faculty:profile']),
            ('createddate', orm['institution.Faculty:createddate']),
            ('updateddate', orm['institution.Faculty:updateddate']),
        ))
        db.send_create_signal('institution', ['Faculty'])
        
        # Adding model 'UserProfile'
        db.create_table('institution_userprofile', (
            ('id', orm['institution.UserProfile:id']),
            ('user', orm['institution.UserProfile:user']),
            ('isadmin', orm['institution.UserProfile:isadmin']),
            ('personalsite', orm['institution.UserProfile:personalsite']),
            ('isFaculty', orm['institution.UserProfile:isFaculty']),
            ('isStudent', orm['institution.UserProfile:isStudent']),
            ('fullname', orm['institution.UserProfile:fullname']),
            ('createddate', orm['institution.UserProfile:createddate']),
            ('updateddate', orm['institution.UserProfile:updateddate']),
            ('approved', orm['institution.UserProfile:approved']),
            ('photo', orm['institution.UserProfile:photo']),
            ('country', orm['institution.UserProfile:country']),
            ('state', orm['institution.UserProfile:state']),
            ('city', orm['institution.UserProfile:city']),
            ('address', orm['institution.UserProfile:address']),
            ('latitude', orm['institution.UserProfile:latitude']),
            ('longitude', orm['institution.UserProfile:longitude']),
        ))
        db.send_create_signal('institution', ['UserProfile'])
        
        # Adding model 'Department'
        db.create_table('institution_department', (
            ('id', orm['institution.Department:id']),
            ('name', orm['institution.Department:name']),
            ('established', orm['institution.Department:established']),
            ('institute', orm['institution.Department:institute']),
            ('createddate', orm['institution.Department:createddate']),
            ('updateddate', orm['institution.Department:updateddate']),
            ('user', orm['institution.Department:user']),
        ))
        db.send_create_signal('institution', ['Department'])
        
        # Adding model 'Institution'
        db.create_table('institution_institution', (
            ('id', orm['institution.Institution:id']),
            ('name', orm['institution.Institution:name']),
            ('website', orm['institution.Institution:website']),
            ('phoneno', orm['institution.Institution:phoneno']),
            ('admin', orm['institution.Institution:admin']),
            ('description', orm['institution.Institution:description']),
            ('subdomain', orm['institution.Institution:subdomain']),
            ('createddate', orm['institution.Institution:createddate']),
            ('updateddate', orm['institution.Institution:updateddate']),
        ))
        db.send_create_signal('institution', ['Institution'])
        
        # Adding model 'Student'
        db.create_table('institution_student', (
            ('id', orm['institution.Student:id']),
            ('whatiamdoing', orm['institution.Student:whatiamdoing']),
            ('company', orm['institution.Student:company']),
            ('title', orm['institution.Student:title']),
            ('industry', orm['institution.Student:industry']),
            ('market', orm['institution.Student:market']),
            ('profile', orm['institution.Student:profile']),
            ('createddate', orm['institution.Student:createddate']),
            ('updateddate', orm['institution.Student:updateddate']),
        ))
        db.send_create_signal('institution', ['Student'])
        
        # Adding model 'Course'
        db.create_table('institution_course', (
            ('id', orm['institution.Course:id']),
            ('name', orm['institution.Course:name']),
            ('introduced', orm['institution.Course:introduced']),
            ('createddate', orm['institution.Course:createddate']),
            ('updateddate', orm['institution.Course:updateddate']),
            ('institute', orm['institution.Course:institute']),
            ('user', orm['institution.Course:user']),
        ))
        db.send_create_signal('institution', ['Course'])
        
        # Adding ManyToManyField 'Course.departments'
        db.create_table('institution_course_departments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm.Course, null=False)),
            ('department', models.ForeignKey(orm.Department, null=False))
        ))
        
        # Adding ManyToManyField 'UserProfile.institutes'
        db.create_table('institution_userprofile_institutes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm.UserProfile, null=False)),
            ('institution', models.ForeignKey(orm.Institution, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'FacultyInstitute'
        db.delete_table('institution_facultyinstitute')
        
        # Deleting model 'StudentInstitute'
        db.delete_table('institution_studentinstitute')
        
        # Deleting model 'Degree'
        db.delete_table('institution_degree')
        
        # Deleting model 'Faculty'
        db.delete_table('institution_faculty')
        
        # Deleting model 'UserProfile'
        db.delete_table('institution_userprofile')
        
        # Deleting model 'Department'
        db.delete_table('institution_department')
        
        # Deleting model 'Institution'
        db.delete_table('institution_institution')
        
        # Deleting model 'Student'
        db.delete_table('institution_student')
        
        # Deleting model 'Course'
        db.delete_table('institution_course')
        
        # Dropping ManyToManyField 'Course.departments'
        db.delete_table('institution_course_departments')
        
        # Dropping ManyToManyField 'UserProfile.institutes'
        db.delete_table('institution_userprofile_institutes')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'institution.course': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['institution.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'introduced': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'institution.degree': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'established': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'institution.department': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'established': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'institution.faculty': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['institution.Institution']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.UserProfile']", 'unique': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'institution.facultyinstitute': {
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Department']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Faculty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'joineddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'specialization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.TextField', [], {})
        },
        'institution.institution': {
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'phoneno': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'institution.student': {
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['statistics.Industry']"}),
            'institutes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['institution.Institution']"}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['statistics.Market']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.UserProfile']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'whatiamdoing': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'institution.studentinstitute': {
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Course']"}),
            'degree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Degree']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Department']"}),
            'fromyear': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'joineddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Student']"}),
            'toyear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'institution.userprofile': {
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Country']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institutes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['institution.Institution']"}),
            'isFaculty': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'isStudent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'isadmin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'personalsite': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'location.country': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'statistics.industry': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'statistics.market': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['statistics.Industry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'unique': 'True'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['institution']
