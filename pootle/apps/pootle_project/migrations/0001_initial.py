# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("pootle_app", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('pootle_app_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('checkstyle', self.gf('django.db.models.fields.CharField')(default='standard', max_length=50)),
            ('localfiletype', self.gf('django.db.models.fields.CharField')(default='po', max_length=50)),
            ('treestyle', self.gf('django.db.models.fields.CharField')(default='auto', max_length=20)),
            ('ignoredfiles', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('directory', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pootle_app.Directory'], unique=True)),
            ('report_target', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('pootle_project', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('pootle_app_project')


    models = {
        'pootle_app.directory': {
            'Meta': {'ordering': "['name']", 'object_name': 'Directory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_dirs'", 'null': 'True', 'to': "orm['pootle_app.Directory']"}),
            'pootle_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'pootle_language.language': {
            'Meta': {'ordering': "['code']", 'object_name': 'Language', 'db_table': "'pootle_app_language'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directory': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pootle_app.Directory']", 'unique': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nplurals': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'pluralequation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'specialchars': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'pootle_project.project': {
            'Meta': {'ordering': "['code']", 'object_name': 'Project', 'db_table': "'pootle_app_project'"},
            'checkstyle': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '50'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directory': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pootle_app.Directory']", 'unique': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignoredfiles': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'localfiletype': ('django.db.models.fields.CharField', [], {'default': "'po'", 'max_length': '50'}),
            'report_target': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'treestyle': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '20'})
        }
    }

    complete_apps = ['pootle_project']
