
class QuerysetFilterService(object):
    """
    A service to process filters applied when browsing map/data.
    """

    def __init__(self, **kwargs):
        if 'network_filter_field' in kwargs:
            self.network_filter_field = kwargs['network_filter_field']
        if 'standard_filter_field' in kwargs:
            self.standard_filter_field = kwargs['standard_filter_field']
        if 'band_filter_field' in kwargs:
            self.band_filter_field = kwargs['band_filter_field']

    def get_processed_filters(self, raw_filters):
        processed_filters = {}
        if 'bounds' in raw_filters:
            bounds_filter = self._get_bounds_filter(raw_filters['bounds'])
            processed_filters.update(bounds_filter)

        if 'network' in raw_filters:
            network_filter = self._get_network_filter(raw_filters['network'])
            processed_filters.update(network_filter)

        standards = []
        if 'standard' in raw_filters:
            standards = raw_filters['standard'].split(',')

        bands = []
        if 'band' in raw_filters:
            bands = raw_filters['band'].split(',')

        if standards or bands:
            standard_band_filter = self._get_standard_band_queryset_filter(
                standards, bands)
            processed_filters.update(standard_band_filter)

        return processed_filters

    def _get_bounds_filter(self, bounds):
        bounds = bounds.split(',')
        return {
            'latitude__gte': bounds[0],
            'longitude__gte': bounds[1],
            'latitude__lte': bounds[2],
            'longitude__lte': bounds[3]
        }

    def _get_network_filter(self, network):
        return {
            self.network_filter_field: network
        }

    def _get_standard_band_queryset_filter(self, standards, bands):
        if standards and bands:
            return {
                self.standard_filter_field: standards,
                self.band_filter_field: bands
            }
        elif standards:
            return {self.standard_filter_field: standards}
        elif bands:
            return {self.band_filter_field: bands}
        return None


class MapIconService(object):
    """
    A service to provide an icon (marker) representing location on the map.

    Work In Progress...
    """
    def get_icon_by_network_code(self, network_code):
        pass

    def get_icon_by_location(self, location, filters):
        pass
