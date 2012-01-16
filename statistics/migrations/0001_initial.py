
from south.db import db
from django.db import models
from statistics.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Market'
        db.create_table('statistics_market', (
            ('id', orm['statistics.Market:id']),
            ('name', orm['statistics.Market:name']),
            ('createddate', orm['statistics.Market:createddate']),
            ('updateddate', orm['statistics.Market:updateddate']),
        ))
        db.send_create_signal('statistics', ['Market'])
        
        # Adding model 'Industry'
        db.create_table('statistics_industry', (
            ('id', orm['statistics.Industry:id']),
            ('name', orm['statistics.Industry:name']),
            ('createddate', orm['statistics.Industry:createddate']),
            ('updateddate', orm['statistics.Industry:updateddate']),
        ))
        db.send_create_signal('statistics', ['Industry'])
        
        # Adding ManyToManyField 'Market.industries'
        db.create_table('statistics_market_industries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('market', models.ForeignKey(orm.Market, null=False)),
            ('industry', models.ForeignKey(orm.Industry, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Market'
        db.delete_table('statistics_market')
        
        # Deleting model 'Industry'
        db.delete_table('statistics_industry')
        
        # Dropping ManyToManyField 'Market.industries'
        db.delete_table('statistics_market_industries')
        
    
    
    models = {
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
    
    complete_apps = ['statistics']
