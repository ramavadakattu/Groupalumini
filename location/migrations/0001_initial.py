
from south.db import db
from django.db import models
from location.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('location_country', (
            ('id', orm['location.Country:id']),
            ('name', orm['location.Country:name']),
        ))
        db.send_create_signal('location', ['Country'])
        
        # Adding model 'State'
        db.create_table('location_state', (
            ('id', orm['location.State:id']),
            ('name', orm['location.State:name']),
            ('country', orm['location.State:country']),
        ))
        db.send_create_signal('location', ['State'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('location_country')
        
        # Deleting model 'State'
        db.delete_table('location_state')
        
    
    
    models = {
        'location.country': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'location.state': {
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['location']
