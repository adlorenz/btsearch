from django.http import Http404
from django.views import generic

from braces.views import JSONResponseMixin

from ..bts import models as bts_models
from ..uke import models as uke_models
from . import utils


class LocationsFilterMixin(object):

    network_filter_field = 'base_stations__network'
    standard_filter_field = 'base_stations__cells__standard__in'
    band_filter_field = 'base_stations__cells__band__in'

    def _get_queryset_filters(self):
        raw_filters = self.request.GET.copy()
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
        # standard_field = 'base_stations__cells__standard__in'
        # band_field = 'base_stations__cells__band__in'

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


class IndexView(generic.TemplateView):
    template_name = 'map/index.html'


class LocationsView(LocationsFilterMixin, JSONResponseMixin, generic.ListView):
    model = bts_models.Location
    queryset = bts_models.Location.objects.distinct()
    paginate_by = 500

    def get(self, request, *args, **kwargs):
        # 'bounds' is a required GET parameter for LocationsView
        if not self.request.GET.get('bounds'):
            raise Http404()

        return self.render_json_response({
            'objects': self._get_locations_list()
        })

    def get_queryset(self):
        qs_filters = self._get_queryset_filters()
        return self.queryset.filter(**qs_filters)

    def _get_locations_list(self):
        raw_filters = dict(self.request.GET.copy())
        locations_list = []
        for location in self.get_queryset():
            locations_list.append({
                'id': location.id,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'icon': self._get_location_icon_path(location, raw_filters),
            })
        return locations_list

    def _get_location_icon_path(self, location, raw_filters):
        # TODO: I don't like this approach. Refactor it.
        map_icon_factory = utils.MapIconFactory()
        map_icon = map_icon_factory.get_icon_by_location(location, raw_filters)
        return map_icon_factory.get_icon_path(map_icon)


class LocationDetailView(LocationsFilterMixin, JSONResponseMixin, generic.DetailView):
    model = bts_models.Location
    template_name = 'map/location_info.html'
    context_object_name = 'location'

    network_filter_field = 'network'
    standard_filter_field = 'cells__standard__in'
    band_filter_field = 'cells__band__in'

    def get_context_data(self, **kwargs):
        ctx = super(LocationDetailView, self).get_context_data(**kwargs)
        ctx['items'] = self._get_location_objects()
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = super(LocationDetailView, self).render_to_response(
            context, **response_kwargs)

        location = self.get_object()
        map_icon = utils.MapIconFactory().get_icon_by_location(location)
        data = {
            'id': location.id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'summary': unicode(location),
            'info': response.render().rendered_content,
            'icon': utils.MapIconFactory().get_icon_path(map_icon),
        }
        return self.render_json_response(data)

    def _get_location_objects(self):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        location = self.get_object()
        qs_filters = self._get_queryset_filters()
        return location.base_stations.distinct().filter(**qs_filters)


class UkeLocationsView(LocationsView):
    model = uke_models.Location
    queryset = uke_models.Location.objects.distinct()

    network_filter_field = 'permissions__operator__network'
    standard_filter_field = 'permissions__standard__in'
    band_filter_field = 'permissions__band__in'


class UkeLocationDetailView(LocationDetailView):
    model = uke_models.Location
    template_name = 'map/uke_location_info.html'

    def _get_location_objects(self):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        location = self.get_object()
        permissions_by_network = {}
        networks = []
        filters = self._get_queryset_filters()
        for permission in location.get_permissions(**filters):
            network = permission.operator.network
            if network not in networks:
                networks.append(network)

            if network.code not in permissions_by_network:
                permissions_by_network[network.code] = []
            permissions_by_network[network.code].append(permission)

        location_objects = []
        for network in networks:
            location_objects.append({
                'network': network,
                'supported': location.get_supported_standards_and_bands_by_network(network),
                'permissions': permissions_by_network[network.code],
            })
        return location_objects


# #####################
# MAP UI ELEMENTS VIEWS
# #####################


class ControlPanelView(generic.TemplateView):
    template_name = 'map/control_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ControlPanelView, self).get_context_data(**kwargs)
        context['networks'] = bts_models.Network.objects.all()
        context['standards'] = bts_models.Cell.STANDARDS
        context['bands'] = bts_models.Cell.BANDS
        return context


class StatusPanelView(generic.TemplateView):
    template_name = 'map/status_panel.html'
