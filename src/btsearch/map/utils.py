from btsearch.bts.models import Location
from btsearch.uke.models import UkeLocation


class MapIconFactory():

    ICON_EXTENSION = '.png'

    def get_icon_by_network(self, network):
        icon_code = self._get_icon_code_from_network_code(network.code)
        return icon_code + self.ICON_EXTENSION

    def get_icon_by_location(self, location, raw_filters):
        """
        Determine icon to render for given location,
        ie. which network operators, hence colours to use.
        """

        # When network filter is present, let's make it quick and clean
        if 'network' in raw_filters:
            icon_code = self._get_icon_code_from_network_code(raw_filters['network'][0])
            return icon_code + self.ICON_EXTENSION

        # Preprocess raw filters
        filters = self.get_processed_filters(raw_filters)

        # Get items (base stations / permission) per location
        location_items = self.get_location_items(location, filters)
        if location_items is None:
            return None

        # Generate code list (a part of icon file name)
        code_list = []
        for item in location_items:
            icon_code = self._get_icon_code_from_network_code(item.network.code)
            if code_list.count(icon_code) == 0:
                code_list.append(icon_code)

        if len(code_list) == 0:
            return None

        # Always put '00' at the end of the lists
        code_list.sort()
        if code_list.count('00') > 0:
            code_list.remove('00')
            code_list.append('00')

        return '_'.join(code_list) + self.ICON_EXTENSION

    def get_location_items(self, location, filters):
        """
        Filter and return location objects (models)
        """
        if isinstance(location, Location):
            return location.get_base_stations(**filters)
        elif isinstance(location, UkeLocation):
            return location.get_permissions(**filters)
        else:
            return None

    def get_processed_filters(self, raw_filters):
        """
        Process raw location filters
        """
        filters = {}
        if 'standard' in raw_filters:
            filters['standard'] = raw_filters['standard'][0].split(',')
        if 'band' in raw_filters:
            filters['band'] = raw_filters['band'][0].split(',')
        return filters

    def _get_icon_code_from_network_code(self, network_code):
        icon_code = network_code[-2:]
        return icon_code if int(icon_code) <= 6 else '00'
