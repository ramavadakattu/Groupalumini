
from south.db import db
from django.db import models
from payments.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Fund'
        db.create_table('payments_fund', (
            ('id', orm['payments.Fund:id']),
            ('fundname', orm['payments.Fund:fundname']),
            ('totalamount', orm['payments.Fund:totalamount']),
            ('totaldonations', orm['payments.Fund:totaldonations']),
            ('description', orm['payments.Fund:description']),
            ('deadline', orm['payments.Fund:deadline']),
            ('currency', orm['payments.Fund:currency']),
            ('institute', orm['payments.Fund:institute']),
            ('user', orm['payments.Fund:user']),
            ('createddate', orm['payments.Fund:createddate']),
            ('updateddate', orm['payments.Fund:updateddate']),
            ('open', orm['payments.Fund:open']),
        ))
        db.send_create_signal('payments', ['Fund'])
        
        # Adding model 'Donation'
        db.create_table('payments_donation', (
            ('id', orm['payments.Donation:id']),
            ('fund', orm['payments.Donation:fund']),
            ('user', orm['payments.Donation:user']),
            ('institute', orm['payments.Donation:institute']),
            ('donationamount', orm['payments.Donation:donationamount']),
            ('createddate', orm['payments.Donation:createddate']),
            ('updateddate', orm['payments.Donation:updateddate']),
            ('paypaltransactionid', orm['payments.Donation:paypaltransactionid']),
            ('correlationid', orm['payments.Donation:correlationid']),
        ))
        db.send_create_signal('payments', ['Donation'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Fund'
        db.delete_table('payments_fund')
        
        # Deleting model 'Donation'
        db.delete_table('payments_donation')
        
    
    
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
        'payments.donation': {
            'correlationid': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'donationamount': ('django.db.models.fields.FloatField', [], {}),
            'fund': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['payments.Fund']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'paypaltransactionid': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'payments.fund': {
            'createddate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fundname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institution.Institution']"}),
            'open': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'totalamount': ('django.db.models.fields.FloatField', [], {}),
            'totaldonations': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updateddate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['payments']
