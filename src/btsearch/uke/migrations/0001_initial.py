# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'uke_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=6, db_index=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=6, db_index=True)),
            ('latitude_uke', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('longitude_uke', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('location_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, db_index=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'uke', ['Location'])

        # Adding model 'Permission'
        db.create_table(u'uke_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', to=orm['uke.Location'])),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', to=orm['uke.Operator'])),
            ('station_id', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('standard', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('band', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('case_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('case_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expiry_date', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'uke', ['Permission'])

        # Adding model 'Operator'
        db.create_table(u'uke_operator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('operator_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uke_operators', to=orm['bts.Network'])),
        ))
        db.send_create_signal(u'uke', ['Operator'])

        # Adding model 'RawRecord'
        db.create_table(u'uke_rawrecord', (
            ('operator_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('case_number', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('case_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expiry_date', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('station_id', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'uke', ['RawRecord'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'uke_location')

        # Deleting model 'Permission'
        db.delete_table(u'uke_permission')

        # Deleting model 'Operator'
        db.delete_table(u'uke_operator')

        # Deleting model 'RawRecord'
        db.delete_table(u'uke_rawrecord')


    models = {
        u'bts.network': {
            'Meta': {'ordering': "['code']", 'object_name': 'Network', 'db_table': "'Bts__Networks'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "'NetworkCode'"}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_column': "'CountryCodeIso'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'NetworkName'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'OperatorName'"})
        },
        u'uke.location': {
            'Meta': {'object_name': 'Location'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6', 'db_index': 'True'}),
            'latitude_uke': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'location_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '6', 'db_index': 'True'}),
            'longitude_uke': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'uke.operator': {
            'Meta': {'object_name': 'Operator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uke_operators'", 'to': u"orm['bts.Network']"}),
            'operator_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'uke.permission': {
            'Meta': {'object_name': 'Permission'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'band': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'case_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['uke.Location']"}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['uke.Operator']"}),
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'station_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'uke.rawrecord': {
            'Meta': {'object_name': 'RawRecord'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'case_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'operator_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'station_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['uke']