# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UkeOperator'
        db.create_table('Uke__OperatorMappings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('operator_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bts.Network'])),
        ))
        db.send_create_signal(u'uke', ['UkeOperator'])


        # Changing field 'UkeRawRecord.operator_name'
        db.alter_column('Uke__RawRecords', 'operator_name', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):
        # Deleting model 'UkeOperator'
        db.delete_table('Uke__OperatorMappings')


        # Changing field 'UkeRawRecord.operator_name'
        db.alter_column('Uke__RawRecords', 'operator_name', self.gf('django.db.models.fields.CharField')(max_length=64))

    models = {
        u'bts.location': {
            'Meta': {'ordering': "['town']", 'object_name': 'Location', 'db_table': "'Bts__Locations'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_column': "'Address'"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'DateAdded'", 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'db_column': "'DateUpdated'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'LocationId'"}),
            'latitude': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'db_column': "'Latitude'", 'blank': 'True'}),
            'latlng_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'LatLngHash'", 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'db_column': "'Longitude'", 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'LocationNotes'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'db_column': "'RegionId'", 'to': u"orm['bts.Region']"}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'Town'"})
        },
        u'bts.network': {
            'Meta': {'ordering': "['code']", 'object_name': 'Network', 'db_table': "'Bts__Networks'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "'NetworkCode'"}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_column': "'CountryCodeIso'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'NetworkName'"}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_column': "'OperatorName'"})
        },
        u'bts.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'Bts__Regions'"},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_column': "'CountryCodeIso'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'RegionId'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'RegionName'"})
        },
        u'uke.ukelocation': {
            'Meta': {'object_name': 'UkeLocation', 'db_table': "'Uke__Locations'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'latlng_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bts.Location']", 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        u'uke.ukeoperator': {
            'Meta': {'object_name': 'UkeOperator', 'db_table': "'Uke__OperatorMappings'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bts.Network']"}),
            'operator_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'uke.ukepermission': {
            'Meta': {'object_name': 'UkePermission', 'db_table': "'Uke__Permissions'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'band': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'case_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['bts.Network']"}),
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'station_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uke_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'to': u"orm['uke.UkeLocation']"})
        },
        u'uke.ukerawrecord': {
            'Meta': {'object_name': 'UkeRawRecord', 'db_table': "'Uke__RawRecords'"},
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