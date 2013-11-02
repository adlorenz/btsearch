# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
from django.views import generic

from braces.views import JSONResponseMixin

from ..bts import models as bts_models
from ..uke import models as uke_models
from . import utils


from django.views.generic import DetailView, TemplateView
from django.template import Context
from django.template.loader import get_template
from settings import STATIC_URL


class IndexView(generic.TemplateView):
    template_name = 'map/index.html'


class LocationsView(JSONResponseMixin, generic.ListView):
    model = bts_models.Location
    queryset = bts_models.Location.objects.distinct()
    paginate_by = 500

    def get(self, request, *args, **kwargs):
        return self.render_json_response({
            'objects': self._get_locations_list()
        })

    def get_queryset(self):
        qs = super(LocationsView, self).get_queryset()
        qs_filters = self._get_queryset_filters()
        return qs.filter(**qs_filters)

    def _get_queryset_filters(self):
        """
        Create map bound local_filters to select locations only relevant to current map view
        """
        filters = self.request.GET.copy()
        if filters is None or 'bounds' not in filters:
            # Reject requests missing 'bounds' filter
            raise Http404()  # TODO: This smells. Refactor it.

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
        map_icon_factory = utils.MapIconFactory()
        map_icon = map_icon_factory.get_icon_by_location(location, raw_filters)
        return map_icon_factory.get_icon_path(map_icon)


class LocationDetailView(JSONResponseMixin, generic.DetailView):
    model = bts_models.Location
    template_name = 'map/location_info.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        ctx = super(LocationDetailView, self).get_context_data(**kwargs)
        ctx['items'] = self._get_location_objects(self.get_object())
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
            'summary': location.__unicode__(),
            'info': response.render().rendered_content,
            'icon': utils.MapIconFactory().get_icon_path(map_icon),
        }
        return self.render_json_response(data)

    def _get_location_objects(self, location):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        filters = self._get_queryset_filters()
        return location.get_base_stations(**filters)

    def _get_queryset_filters(self):
        raw_filters = dict(self.request.GET.copy())
        queryset_filters = {}
        for key in ['standard', 'band']:
            if key in raw_filters:
                queryset_filters.update({
                    key: raw_filters[key][0].split(',')
                })
        return queryset_filters


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


# ################
# DEPRECATED VIEWS
# ################


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