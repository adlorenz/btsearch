# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'UkeLocation', fields ['latlng_hash']
        db.create_index('Uke__Locations', ['latlng_hash'])

        # Adding index on 'UkeLocation', fields ['longitude']
        db.create_index('Uke__Locations', ['longitude'])

        # Adding index on 'UkeLocation', fields ['latitude']
        db.create_index('Uke__Locations', ['latitude'])

        # Adding index on 'UkePermission', fields ['station_id']
        db.create_index('Uke__Permissions', ['station_id'])

        # Adding index on 'UkePermission', fields ['standard']
        db.create_index('Uke__Permissions', ['standard'])

        # Adding index on 'UkePermission', fields ['band']
        db.create_index('Uke__Permissions', ['band'])

        # Adding index on 'UkePermission', fields ['case_number']
        db.create_index('Uke__Permissions', ['case_number'])


    def backwards(self, orm):
        # Removing index on 'UkePermission', fields ['case_number']
        db.delete_index('Uke__Permissions', ['case_number'])

        # Removing index on 'UkePermission', fields ['band']
        db.delete_index('Uke__Permissions', ['band'])

        # Removing index on 'UkePermission', fields ['standard']
        db.delete_index('Uke__Permissions', ['standard'])

        # Removing index on 'UkePermission', fields ['station_id']
        db.delete_index('Uke__Permissions', ['station_id'])

        # Removing index on 'UkeLocation', fields ['latitude']
        db.delete_index('Uke__Locations', ['latitude'])

        # Removing index on 'UkeLocation', fields ['longitude']
        db.delete_index('Uke__Locations', ['longitude'])

        # Removing index on 'UkeLocation', fields ['latlng_hash']
        db.delete_index('Uke__Locations', ['latlng_hash'])


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
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bts.Network']"}),
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'station_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uke_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uke.UkeLocation']"})
        },
        u'uke.ukerawrecord': {
            'Meta': {'object_name': 'UkeRawRecord', 'db_table': "'Uke__RawRecords'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'case_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'expiry_date': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'operator_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'station_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['uke']