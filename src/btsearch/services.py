import arrow
import hashlib

from django.conf import settings


class QuerysetFilterService(object):
    """
    A service to process filters applied when browsing map/data.
    """
    skip_bounds_filter = False

    def get_processed_filters(self, raw_filters):
        processed_filters = {}
        if 'bounds' in raw_filters and not self.skip_bounds_filter:
            processed_filters.update(
                self._get_bounds_filter(raw_filters['bounds'])
            )

        if 'network' in raw_filters and raw_filters['network']:
            processed_filters.update(
                self._get_network_filter(raw_filters['network'])
            )

        if 'region' in raw_filters and raw_filters['region']:
            processed_filters.update(
                self._get_region_filter(raw_filters['region'])
            )

        if 'timedelta' in raw_filters and raw_filters['timedelta']:
            processed_filters.update(
                self._get_timedelta_filter(raw_filters['timedelta'])
            )

        standards = []
        if 'standard' in raw_filters and raw_filters['standard']:
            standards = raw_filters['standard'].split(',')

        bands = []
        if 'band' in raw_filters and raw_filters['band']:
            bands = raw_filters['band'].split(',')

        if standards or bands:
            processed_filters.update(
                self._get_standard_band_queryset_filter(standards, bands)
            )

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

    def _get_region_filter(self, region):
        return {
            self.region_filter_field: region
        }

    def _get_timedelta_filter(self, timedelta):
        # timedelta is a number of days
        delta = arrow.now().replace(days=-int(timedelta))
        return {
            self.timedelta_filter_field: delta.format('YYYY-MM-DD HH:mm:ss')
        }

    def _get_standard_band_queryset_filter(self, standards, bands):
        if standards and bands:
            return {
                self.standard_filter_field: standards,
                self.band_filter_field: bands
            }
        elif standards:
            return {
                self.standard_filter_field: standards
            }
        elif bands:
            return {
                self.band_filter_field: bands
            }
        return None


class BtsLocationsFilterService(QuerysetFilterService):
    network_filter_field = 'base_stations__network'
    standard_filter_field = 'base_stations__cells__standard__in'
    band_filter_field = 'base_stations__cells__band__in'
    timedelta_filter_field = 'base_stations__date_updated__gte'


class BtsLocationFilterService(QuerysetFilterService):
    network_filter_field = 'network'
    standard_filter_field = 'cells__standard__in'
    band_filter_field = 'cells__band__in'
    region_filter_field = 'location__region'
    timedelta_filter_field = 'date_updated__gte'
    skip_bounds_filter = True


class UkeLocationsFilterService(QuerysetFilterService):
    network_filter_field = 'permissions__operator__network'
    standard_filter_field = 'permissions__standard__in'
    band_filter_field = 'permissions__band__in'
    timedelta_filter_field = 'permissions__date_added__gte'


class UkeLocationFilterService(QuerysetFilterService):
    network_filter_field = 'operator__network'
    standard_filter_field = 'standard__in'
    band_filter_field = 'band__in'
    timedelta_filter_field = 'date_added__gte'
    skip_bounds_filter = True


class MapIconService():
    """
    A service to provide an icon (marker) representing location on the map.
    """
    full_path = True

    def get_icon_by_network(self, network):
        return self.get_icon_by_network_code(network.code)

    def get_icon_by_network_code(self, network_code):
        icon_code = self._get_icon_code_from_network_code(network_code) \
            if network_code != '26034' else '34'  # 26034 (NetWorks!) is a special case
        return self._get_icon_path(icon_code)

    def get_icon_by_location(self, location, filter_service=None, raw_filters=[]):

        # Network filter makes it easy
        if 'network' in raw_filters and raw_filters['network']:
            return self.get_icon_by_network_code(raw_filters['network'])

        # Apply filters if specified
        if filter_service:
            qs_filters = filter_service.get_processed_filters(raw_filters)
            location_objects = location.get_associated_objects(**qs_filters)
        else:
            location_objects = location.get_associated_objects()

        # Jump off the train if no wagons are around
        if not location_objects:
            return None

        # Generate list of icon codes from network codes
        location_objects = location_objects.values('network')  # Incredibly improves DB performance!
        icon_codes_list = []
        for obj in location_objects:
            icon_code = self._get_icon_code_from_network_code(obj.get('network'))
            if icon_code not in icon_codes_list:
                icon_codes_list.append(icon_code)

        # Special case for 26034 (NetWorks!)
        # In case NetWorks! icon in the list, make sure that 26002 (TMPL)
        # and 26003 (Orange) are always displayed
        if '34' in icon_codes_list:
            icon_codes_list.append('02')
            icon_codes_list.append('03')
            icon_codes_list.remove('34')
            icon_codes_list = list(set(icon_codes_list))

        # Sort list and always put '00' code at the end of the list
        icon_codes_list.sort()
        if '00' in icon_codes_list:
            icon_codes_list.remove('00')
            icon_codes_list.append('00')

        return self._get_icon_path('_'.join(icon_codes_list))

    def _get_icon_path(self, icon_code):
        if self.full_path:
            return "{0}{1}.png".format(settings.MAP_ICON_PATH, icon_code)
        return icon_code

    def _get_icon_code_from_network_code(self, network_code):
        # A shortcut method to get icons straight by network code,
        # as icons are named after network codes (up to code 06,
        # all above networks share same icon)
        if network_code:
            icon_code = network_code[-2:]
            int_code = int(icon_code)
            # Special case for '34' (NetWorks!)
            return icon_code if int_code <= 6 or int_code == 34 else '00'
        return '00'


class LocationHasherService():
    """
    Calculate location md5 hash from geo coordinates.
    """
    def __init__(self, latitude, longitude):
        self.latitude = str(latitude)
        self.longitude = str(longitude)

    def get(self):
        string = "{0}{1}".format(
            self.latitude,
            self.longitude
        )
        return hashlib.md5(string).hexdigest()
