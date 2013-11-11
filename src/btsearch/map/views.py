from django.http import Http404
from django.views import generic

from braces.views import JSONResponseMixin

from ..bts import models as bts_models
from ..uke import models as uke_models
from . import services
from . import utils


class LocationsFilterMixin(object):

    def get_queryset_filters(self):
        filter_service = services.QuerysetFilterService(
            network_filter_field=self.network_filter_field,
            standard_filter_field=self.standard_filter_field,
            band_filter_field=self.band_filter_field,
        )
        raw_filters = self.request.GET.copy()
        return filter_service.get_processed_filters(raw_filters)


class IndexView(generic.TemplateView):
    template_name = 'map/index.html'


class LocationsView(LocationsFilterMixin, JSONResponseMixin, generic.ListView):
    model = bts_models.Location
    queryset = bts_models.Location.objects.distinct()
    paginate_by = 500

    network_filter_field = 'base_stations__network'
    standard_filter_field = 'base_stations__cells__standard__in'
    band_filter_field = 'base_stations__cells__band__in'

    def get(self, request, *args, **kwargs):
        # 'bounds' is a required GET parameter for LocationsView
        if not self.request.GET.get('bounds'):
            raise Http404()

        return self.render_json_response({
            'objects': self._get_locations_list()
        })

    def get_queryset(self):
        qs_filters = self.get_queryset_filters()
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
        qs_filters = self.get_queryset_filters()
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

    network_filter_field = 'operator__network'
    standard_filter_field = 'standard__in'
    band_filter_field = 'band__in'

    def _get_location_objects(self):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        # TODO: It's slightly messy. Do something about it.
        permissions_by_network = {}
        networks = []
        location = self.get_object()
        qs_filters = self.get_queryset_filters()
        permissions = location.permissions.distinct().filter(**qs_filters)
        for permission in permissions:
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
