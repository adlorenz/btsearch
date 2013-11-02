from django.http import Http404
from django.views import generic

from ..bts import models as bts_models
from ..uke import models as uke_models


from django.views.generic import DetailView, TemplateView
from django.template import Context
from django.template.loader import get_template
from settings import STATIC_URL
from btsearch.bts.models import BaseStation, Cell, Network
from btsearch.uke.models import UkeLocation, UkePermission


class BtsLocationsView(generic.ListView):
    model = bts_models.Location
    queryset = bts_models.Location.objects.distinct()

    def get_queryset(self):
        qs = super(BtsLocationsView, self).get_queryset()
        qs_filters = self._get_queryset_filters()
        return qs.filter(**qs_filters)

    def _get_queryset_filters(self):
        """
        Create map bound local_filters to select locations only relevant to current map view
        """
        filters = self.request.GET.copy()
        if filters is None or 'bounds' not in filters:
            # Reject requests missing 'bounds' filter
            raise Http404()

        # self.raw_filters = dict(filters)
        processed_filters = {}

        bounds = filters['bounds'].split(',')
        processed_filters.update({
            'latitude__gte': bounds[0],
            'longitude__gte': bounds[1],
            'latitude__lte': bounds[2],
            'longitude__lte': bounds[3]
        })

        if 'network' in filters:
            processed_filters.update({
                'basestation__network': filters['network']
            })

        standards = []
        if 'standard' in filters:
            standards = filters['standard'].split(',')

        bands = []
        if 'band' in filters:
            bands = filters['band'].split(',')

        standard_band_filter = self._get_standard_band_queryset_filter(standards, bands)
        if standard_band_filter:
            processed_filters.update(standard_band_filter)

        return processed_filters

    def _get_standard_band_queryset_filter(self, standards, bands):
        standard_field = 'base_stations__cell__standard__in'
        band_field = 'base_stations__cell__band__in'

        if standards and bands:
            return {standard_field: standards, band_field: bands}
        elif standards:
            return {standard_field: standards}
        elif bands:
            return {band_field: bands}
        return None


class IndexView(TemplateView):
    template_name = 'map/index.html'


class ControlPanelView(TemplateView):
    template_name = 'map/control_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ControlPanelView, self).get_context_data(**kwargs)
        context['networks'] = Network.objects.all()
        context['standards'] = Cell.STANDARDS
        context['bands'] = Cell.BANDS
        return context


class StatusPanelView(TemplateView):
    template_name = 'map/status_panel.html'



class LocationView():
    template_name = 'map/location_info.html'
    location = None
    raw_filters = {}

    def __init__(self, location, raw_filters):
        self.location = location
        self.raw_filters = raw_filters

    def get_location_items(self):
        filters = self.get_processed_filters()
        return self.location.get_base_stations(**filters)

    def get_processed_filters(self):
        filters = {}
        if 'standard' in self.raw_filters:
            filters['standard'] = self.raw_filters['standard'][0].split(',')
        if 'band' in self.raw_filters:
            filters['band'] = self.raw_filters['band'][0].split(',')
        return filters

    def render_location_info(self):
        template = get_template(self.template_name)
        context = {'location': self.location,
                   'items': self.get_location_items(),
                   'STATIC_URL': STATIC_URL}
        return template.render(Context(context))


class UkeLocationView(LocationView):
    template_name = 'map/uke_location_info.html'

    def get_location_items(self):
        permissions_by_network = {}
        networks = []
        filters = self.get_processed_filters()
        for permission in self.location.get_permissions(**filters):
            network = permission.network
            if network not in networks:
                networks.append(network)

            if not permissions_by_network.has_key(network.code):
                permissions_by_network[network.code] = []
            permissions_by_network[network.code].append(permission)

        items = []
        for network in networks:
            items.append({'network': network,
                          'supported': self.location.get_supported_standards_and_bands_by_network(network),
                          'permissions': permissions_by_network[network.code]})
        return items