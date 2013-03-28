from settings import STATIC_URL
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import InvalidFilterError
from tastypie.resources import ModelResource
from django.db.models import Q
from btsearch.bts.models import Location
from btsearch.uke.models import UkeLocation
from btsearch.map.views import LocationView, UkeLocationView
from btsearch.map.utils import MapIconFactory

class LocalhostAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        return True
    
        # TODO: Only ajax requests originated from the same host should
        # be allowed to access this API
        
        #if request.META.get('REMOTE_ADDR') != '127.0.0.1':
        #    return request.is_ajax()
        

class LocationResource(ModelResource):
    
    raw_filters = {}
    filter_prefixes = {'network': 'basestation__',
                       'standard': 'basestation__cell__',
                       'band': 'basestation__cell__'}
    
    icon = fields.CharField()
    summary = fields.CharField()
    
    class Meta:
        authentication = LocalhostAuthentication()
        queryset = Location.objects.distinct()
        resource_name = 'locations'
        fields = ['id', 'latitude', 'longitude', 'name']
        include_resource_uri = False
        limit = 500
        
    def alter_detail_data_to_serialize(self, request, data):
        """
        In single location request, append rendered html for infoWindow bubble
        """
        data.data['info'] = LocationView(data.obj, self.raw_filters).render_location_info()
        return data
        
    def build_filters(self, filters=None):
        """
        Create map bound local_filters to select locations only relevant to current map view
        """
        if filters is None or 'bounds' not in filters:
            # Reject requests missing 'bounds' filter
            raise InvalidFilterError("Bounds parameter missing: ?bounds=lat_lo,lng_lo,lat_hi,lng_hi")
        
        self.raw_filters = dict(filters) # To be used by dehydrate_icon() method
        processed_filters = {}
        
        bounds = filters['bounds'].split(',')
        bounds_filter = self.get_bounds_filter(bounds)
        processed_filters.update(bounds_filter)
        
        if 'network' in filters:
            network_filter = self.get_network_filter(filters['network'])
            processed_filters.update(network_filter)
            
        standards = []
        if 'standard' in filters:
            standards = filters['standard'].split(',')

        bands = []
        if 'band' in filters:
            bands = filters['band'].split(',')
            
        standard_band_filter = self.get_standard_band_filter(standards, bands)
        if standard_band_filter is not None:
            processed_filters.update(standard_band_filter)
        
        return processed_filters
        
    def get_bounds_filter(self, bounds):
        return {'latitude__gte': bounds[0],
                'longitude__gte': bounds[1],
                'latitude__lte': bounds[2],
                'longitude__lte': bounds[3]}
    
    def get_network_filter(self, network):
        network_field = self.filter_prefixes['network'] + 'network'
        return {network_field: network}
    
    def get_standard_band_filter(self, standards, bands):
        standard_field = self.filter_prefixes['standard'] + 'standard__in'
        band_field = self.filter_prefixes['band'] + 'band__in'
        
        if len(standards) > 0 and len(bands) > 0:
            return {standard_field: standards, band_field: bands}
        elif len(standards) > 0:
            return {standard_field: standards}
        elif len(bands) > 0:
            return {band_field: bands}
        return None
        

    def dehydrate_icon(self, bundle):
        """
        Create marker icon path for current location
        """
        map_icon = MapIconFactory().get_icon_by_location(bundle.obj, self.raw_filters)
        if map_icon is not None:
            return STATIC_URL + 'map_icons/' + map_icon
        return None
        
    def dehydrate_summary(self, bundle):
        return bundle.obj.__unicode__()
    
    
    
class UkeLocationResource(LocationResource):
    
    filter_prefixes = {'network': 'ukepermission__',
                       'standard': 'ukepermission__',
                       'band': 'ukepermission__'}
    
    icon = fields.CharField()
    summary = fields.CharField()
    
    class Meta:
        authentication = LocalhostAuthentication()
        queryset = UkeLocation.objects.distinct()
        resource_name = 'ukelocations'
        fields = ['id', 'latitude', 'longitude']
        include_resource_uri = False
        limit = 500

    def alter_detail_data_to_serialize(self, request, data):
        """
        In single location request, append rendered html for infoWindow bubble
        """
        data.data['info'] = UkeLocationView(data.obj, self.raw_filters).render_location_info()
        return data
