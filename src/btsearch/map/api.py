from django.conf import settings

from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.exceptions import InvalidFilterError
from tastypie.resources import ModelResource

from ..bts import models as bts_models
from ..uke import models as uke_models
from . import views
from . import utils


"""
This is a tastypie-driven API for the map UI. It's fairly straightforward,
implements two resources which provide data for the map. It has been written
during a short but intense affection to django-tastypie around 2012.
It probably could be simplified/refactored/rewritten but does the job
sufficiently for time being.
"""


class LocalhostAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # TODO: Only ajax requests originated from the same host should
        # be allowed to access this API (by checking request object?)
        return True


class LocationResource(ModelResource):

    raw_filters = {}
    filter_prefixes = {
        'network': 'basestation__',
        'standard': 'basestation__cell__',
        'band': 'basestation__cell__'
    }
    icon = fields.CharField()
    summary = fields.CharField()

    class Meta:
        authentication = LocalhostAuthentication()
        queryset = bts_models.Location.objects.distinct()
        resource_name = 'locations'
        fields = ['id', 'latitude', 'longitude', 'name']
        include_resource_uri = False
        limit = 500

    def alter_detail_data_to_serialize(self, request, data):
        """
        In single location request, append rendered html for infoWindow bubble
        """
        data.data['info'] = views.LocationView(data.obj, self.raw_filters).render_location_info()
        return data

    def build_filters(self, filters=None):
        """
        Create map bound local_filters to select locations only relevant to current map view
        """
        if filters is None or 'bounds' not in filters:
            # Reject requests missing 'bounds' filter
            raise InvalidFilterError("Bounds parameter missing: ?bounds=lat_lo,lng_lo,lat_hi,lng_hi")

        self.raw_filters = dict(filters)  # To be used by dehydrate_icon() method
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
        return {
            'latitude__gte': bounds[0],
            'longitude__gte': bounds[1],
            'latitude__lte': bounds[2],
            'longitude__lte': bounds[3]
        }

    def get_network_filter(self, network):
        network_field = '{0}network'.format(self.filter_prefixes['network'])
        return {network_field: network}

    def get_standard_band_filter(self, standards, bands):
        standard_field = '{0}standard__in'.format(self.filter_prefixes['standard'])
        band_field = '{0}band__in'.format(self.filter_prefixes['band'])

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
        map_icon = utils.MapIconFactory().get_icon_by_location(bundle.obj, self.raw_filters)
        if map_icon is not None:
            return "{0}map_icons/{1}".format(settings.STATIC_URL, map_icon)
        return None

    def dehydrate_summary(self, bundle):
        return bundle.obj.__unicode__()


class UkeLocationResource(LocationResource):

    filter_prefixes = {
        'network': 'ukepermission__',
        'standard': 'ukepermission__',
        'band': 'ukepermission__'
    }
    icon = fields.CharField()
    summary = fields.CharField()

    class Meta:
        authentication = LocalhostAuthentication()
        queryset = uke_models.UkeLocation.objects.distinct()
        resource_name = 'ukelocations'
        fields = ['id', 'latitude', 'longitude']
        include_resource_uri = False
        limit = 500

    def alter_detail_data_to_serialize(self, request, data):
        """
        In single location request, append rendered html for infoWindow bubble
        """
        data.data['info'] = views.UkeLocationView(data.obj, self.raw_filters).render_location_info()
        return data
