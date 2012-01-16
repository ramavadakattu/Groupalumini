
from south.db import db
from django.db import models
from askalumini.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('askalumini_question', (
            ('id', orm['askalumini.Question:id']),
            ('subject', orm['askalumini.Question:subject']),
            ('description', orm['askalumini.Question:description']),
            ('createddate', orm['askalumini.Question:createddate']),
            ('updateddate', orm['askalumini.Question:updateddate']),
            ('institute', orm['askalumini.Question:institute']),
            ('user', orm['askalumini.Question:user']),
        ))
        db.send_create_signal('askalumini', ['Question'])
        
        # Adding model 'Comment'
        db.create_table('askalumini_comment', (
            ('id', orm['askalumini.Comment:id']),
            ('text', orm['askalumini.Comment:text']),
            ('createddate', orm['askalumini.Comment:createddate']),
            ('updateddate', orm['askalumini.Comment:updateddate']),
            ('user', orm['askalumini.Comment:user']),
            ('content_type', orm['askalumini.Comment:content_type']),
            ('object_id', orm['askalumini.Comment:object_id']),
        ))
        db.send_create_signal('askalumini', ['Comment'])
        
        # Adding model 'Answer'
        db.create_table('askalumini_answer', (
            ('id', orm['askalumini.Answer:id']),
            ('text', orm['askalumini.Answer:text']),
            ('createddate', orm['askalumini.Answer:createddate']),
            ('updateddate', orm['askalumini.Answer:updateddate']),
            ('user', orm['askalumini.Answer:user']),
            ('question', orm['askalumini.Answer:question']),
        ))
        db.send_create_signal('askalumini', ['Answer'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Question'
        db.delete_table('askalumini_question')
        
        # Deleting model 'Comment'
        db.delete_table('askalumini_comment')
        
        # Deleting model 'Answer'
        db.delete_table('askalumini_answer')
        
    
    
    models = {
        'askalumini.answer': {
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['askalumini.Comment']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askalumini.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'askalumini.comment': {
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'askalumini.question': {
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['askalumini.Comment']"}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
        }
    }
    
    complete_apps = ['askalumini']
