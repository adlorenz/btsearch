from django.contrib import admin
from btsearch.bts.models import BaseStation, Network, Cell, Location, Region, LegacyBaseStation
from btsearch.bts.admin_forms import LocationAdminForm, BaseStationAdminForm

class BaseStationInline(admin.TabularInline):
    model = BaseStation
    extra = 0

class CellInline(admin.TabularInline):
    model = Cell
    extra = 0

class BaseStationAdmin(admin.ModelAdmin):
    form = BaseStationAdminForm
    fields = ('location_info','location_selected', 'location', 'location_details', 'network', 'station_id', 'rnc', 'is_common_bcch', 'is_gsm', 'is_umts', 'is_cdma', 'is_lte', 'notes', 'station_status', 'edit_status', 'date_added', 'date_updated','location_coords')
    inlines = [CellInline]
    list_display = ['id', 'network', 'region_name', 'town_name', 'address_name', 'station_status', 'edit_status']
    list_filter = ['network', 'location__region', 'station_status', 'edit_status']
    readonly_fields = ['date_added', 'date_updated']
    save_on_top = True
    search_fields = ['=id', 'location__town', 'location__address']

class CellAdmin(admin.ModelAdmin):
    list_display = ['id', 'base_station', 'standard', 'band', 'lac', 'cid', 'is_confirmed']
    list_filter = ['standard', 'band', 'base_station__network']
    readonly_fields = ['base_station', 'date_added', 'date_updated', 'date_ping']
    save_on_top = True
    search_fields = ['=lac', '=cid', '=cid_long', 'base_station__location__town']
    
class LocationAdmin(admin.ModelAdmin):
    #fields = ['region', 'town', 'address', 'notes', 'latitude', 'longitude', 'gps_hash']
    form = LocationAdminForm
    inlines = [BaseStationInline]
    list_display = ['id', 'region', 'town', 'address', 'has_latlng_hash']
    list_filter = ['region']
    save_on_top = True
    search_fields = ['=id', 'town', 'address']
    readonly_fields = ['latlng_hash', 'date_added', 'date_updated']
    
#class UkeLocationAdmin(admin.ModelAdmin):
#    model = UkeLocation
#    list_display = ['station_id', 'network', 'location', 'location_details', 'band', 'case_number']
#    list_filter = ['network', 'band']
#    readonly_fields = ['station_id', 'network', 'location', 'location_details', 'band', 'band_all', 'latitude', 'longitude', 'latlng_hash', 'case_number']
    
class LegacyBaseStationAdmin(admin.ModelAdmin):
    list_display = ['id', 'network', 'region', 'town', 'location', 'standard', 'band', 'lac', 'btsid', 'station_id']
    list_filter = ['network', 'region', 'standard']
    search_fields = ['=id', 'town', 'location', 'btsid']

admin.site.register(BaseStation, BaseStationAdmin)
admin.site.register(Network)
admin.site.register(Cell, CellAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Region)
#admin.site.register(UkeLocation, UkeLocationAdmin)
admin.site.register(LegacyBaseStation, LegacyBaseStationAdmin)