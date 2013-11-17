# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Permission.network'
        db.add_column(u'uke_permission', 'network',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='permissions', null=True, to=orm['bts.Network']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Permission.network'
        db.delete_column(u'uke_permission', 'network_id')


    models = {
        u'bts.network': {
            'Meta': {'ordering': "['code']", 'object_name': 'Network'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'operator_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'uke.location': {
            'Meta': {'ordering': "['id']", 'object_name': 'Location'},
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
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permissions'", 'null': 'True', 'to': u"orm['bts.Network']"}),
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