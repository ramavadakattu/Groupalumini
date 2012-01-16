
from south.db import db
from django.db import models
from feedback.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Feedback'
        db.create_table('feedback_feedback', (
            ('id', orm['feedback.Feedback:id']),
            ('email', orm['feedback.Feedback:email']),
            ('username', orm['feedback.Feedback:username']),
            ('message', orm['feedback.Feedback:message']),
        ))
        db.send_create_signal('feedback', ['Feedback'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Feedback'
        db.delete_table('feedback_feedback')
        
    
    
    models = {
        'feedback.feedback': {
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['feedback']
