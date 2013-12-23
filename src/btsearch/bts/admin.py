from django.contrib import admin

from . import models
from . import admin_forms


class BaseStationInline(admin.TabularInline):
    model = models.BaseStation
    extra = 0


class CellInline(admin.TabularInline):
    model = models.Cell
    extra = 0
    fields = (
        'standard',
        'band',
        'ua_freq',
        'lac',
        'cid',
        'ecid',
        'azimuth',
        'is_confirmed',
        'notes',
    )


class BaseStationAdmin(admin.ModelAdmin):
    form = admin_forms.BaseStationAdminForm
    inlines = [CellInline]
    fields = (
        'location_info',
        'location_selected',
        'location',
        'location_details',
        'network',
        'station_id',
        'rnc',
        'enbi',
        'is_common_bcch',
        'is_gsm',
        'is_umts',
        'is_cdma',
        'is_lte',
        'is_networks',
        'notes',
        'station_status',
        'edit_status',
        'date_added',
        'date_updated',
        'location_coords'
    )
    list_display = [
        'id',
        'network',
        'station_id',
        'region_name',
        'town_name',
        'address_name',
        'station_status',
        'edit_status'
    ]
    list_filter = [
        'network',
        'location__region',
        'station_status',
        'edit_status'
    ]
    readonly_fields = [
        'date_added',
        'date_updated'
    ]
    search_fields = [
        '=id',
        'location__town',
        'location__address',
        'station_id'
    ]
    save_on_top = True


class CellAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'network_name',
        'standard',
        'band',
        'lac',
        'cid',
        'is_confirmed'
    ]
    list_filter = [
        'standard',
        'band',
        'base_station__network'
    ]
    readonly_fields = [
        'base_station',
        'date_added',
        'date_updated',
        'date_ping'
    ]
    search_fields = [
        '=lac',
        '=cid',
        '=cid_long',
        '=ecid',
        'base_station__location__town'
    ]
    save_on_top = True


class LocationAdmin(admin.ModelAdmin):
    #fields = ['region', 'town', 'address', 'notes', 'latitude', 'longitude', 'gps_hash']
    form = admin_forms.LocationAdminForm
    inlines = [BaseStationInline]
    list_display = [
        'id',
        'region',
        'town',
        'address',
        'has_location_hash'
    ]
    list_filter = ['region']
    search_fields = [
        '=id',
        'town',
        'address'
    ]
    readonly_fields = [
        'location_hash',
        'date_added',
        'date_updated'
    ]
    save_on_top = True

#class UkeLocationAdmin(admin.ModelAdmin):
#    model = UkeLocation
#    list_display = ['station_id', 'network', 'location', 'location_details', 'band', 'case_number']
#    list_filter = ['network', 'band']
#    readonly_fields = ['station_id', 'network', 'location', 'location_details', 'band', 'band_all', 'latitude', 'longitude', 'latlng_hash', 'case_number']


# class LegacyBaseStationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'network', 'region', 'town', 'location', 'standard', 'band', 'lac', 'btsid', 'station_id']
#     list_filter = ['network', 'region', 'standard']
#     search_fields = ['=id', 'town', 'location', 'btsid']


admin.site.register(models.BaseStation, BaseStationAdmin)
admin.site.register(models.Network)
admin.site.register(models.Cell, CellAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Region)
#admin.site.register(UkeLocation, UkeLocationAdmin)
# admin.site.register(LegacyBaseStation, LegacyBaseStationAdmin)
