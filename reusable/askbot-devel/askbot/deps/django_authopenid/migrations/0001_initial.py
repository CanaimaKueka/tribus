# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Nonce'
        db.create_table('django_authopenid_nonce', (
            ('timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_authopenid', ['Nonce'])

        # Adding model 'Association'
        db.create_table('django_authopenid_association', (
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')()),
            ('server_url', self.gf('django.db.models.fields.TextField')(max_length=2047)),
            ('assoc_type', self.gf('django.db.models.fields.TextField')(max_length=64)),
            ('secret', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('django_authopenid', ['Association'])

        # Adding model 'UserAssociation'
        db.create_table('django_authopenid_userassociation', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('openid_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('django_authopenid', ['UserAssociation'])

        # Adding model 'UserPasswordQueue'
        db.create_table('django_authopenid_userpasswordqueue', (
            ('new_password', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('confirm_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('django_authopenid', ['UserPasswordQueue'])

        # Adding model 'ExternalLoginData'
        db.create_table('django_authopenid_externallogindata', (
            ('external_username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_session_data', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('django_authopenid', ['ExternalLoginData'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Nonce'
        db.delete_table('django_authopenid_nonce')

        # Deleting model 'Association'
        db.delete_table('django_authopenid_association')

        # Deleting model 'UserAssociation'
        db.delete_table('django_authopenid_userassociation')

        # Deleting model 'UserPasswordQueue'
        db.delete_table('django_authopenid_userpasswordqueue')

        # Deleting model 'ExternalLoginData'
        db.delete_table('django_authopenid_externallogindata')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bronze': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_isvalid': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gold': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'gravatar': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'hide_ignored_questions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'questions_per_page': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'response_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'silver': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '2'}),
            'tag_filter_setting': ('django.db.models.fields.CharField', [], {'default': "'ignored'", 'max_length': '16'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_authopenid.association': {
            'Meta': {'object_name': 'Association'},
            'assoc_type': ('django.db.models.fields.TextField', [], {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.TextField', [], {'max_length': '2047'})
        },
        'django_authopenid.externallogindata': {
            'Meta': {'object_name': 'ExternalLoginData'},
            'external_session_data': ('django.db.models.fields.TextField', [], {}),
            'external_username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'django_authopenid.nonce': {
            'Meta': {'object_name': 'Nonce'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'django_authopenid.userassociation': {
            'Meta': {'object_name': 'UserAssociation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'openid_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'django_authopenid.userpasswordqueue': {
            'Meta': {'object_name': 'UserPasswordQueue'},
            'confirm_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_password': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['django_authopenid']
