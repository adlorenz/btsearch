from django.http import Http404
from django.views import generic

from braces.views import JSONResponseMixin

from ..bts import models as bts_models
from ..uke import models as uke_models
from .. import mixins
from .. import services


class IndexView(generic.TemplateView):
    template_name = 'map/index.html'


class LocationsView(mixins.QuerysetFilterMixin, JSONResponseMixin, generic.ListView):
    model = bts_models.Location
    queryset = bts_models.Location.objects.distinct()
    filter_class = services.BtsLocationsFilterService
    return_empty_locations = False

    def get(self, request, *args, **kwargs):
        # 'bounds' is a required GET parameter for LocationsView
        if not self.request.GET.get('bounds'):
            raise Http404()

        # Allow returning locations that don't have any base stations assigned
        self.return_empty_locations = 'empty' in request.GET.copy()

        return self.render_json_response({
            'objects': self._get_locations_list()
        })

    def get_queryset(self):
        qs_filters = self.get_queryset_filters()
        # Poor-man's hard limit of 500 results to improve performance
        return self.queryset.filter(**qs_filters)[:500]

    def _get_single_location_filter_class(self):
        return services.BtsLocationFilterService

    def _get_locations_list(self):
        icon_service = services.MapIconService()
        filter_class = self._get_single_location_filter_class()
        raw_filters = self.request.GET.copy()
        locations_list = []
        locations = self.get_queryset()
        for location in locations:
            location_icon = icon_service.get_icon_by_location(
                location,
                filter_class(),
                raw_filters
            )
            if self.return_empty_locations or location_icon:
                locations_list.append({
                    'id': location.id,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'icon': location_icon,
                })
        return locations_list


class LocationDetailView(mixins.QuerysetFilterMixin, JSONResponseMixin, generic.DetailView):
    model = bts_models.Location
    template_name = 'popups/location_bts.html'
    context_object_name = 'location'
    filter_class = services.BtsLocationFilterService

    def get_context_data(self, **kwargs):
        ctx = super(LocationDetailView, self).get_context_data(**kwargs)
        ctx['items'] = self._get_location_objects()
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response = super(LocationDetailView, self).render_to_response(
            context, **response_kwargs)

        location = self.get_object()
        data = {
            'id': location.id,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'summary': str(location),
            'info': response.render().rendered_content,
            'icon': services.MapIconService().get_icon_by_location(location),
        }
        return self.render_json_response(data)

    def _get_location_objects(self):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        location = self.get_object()
        qs_filters = self.get_queryset_filters()
        return location.get_associated_objects(**qs_filters)


class UkeLocationsView(LocationsView):
    model = uke_models.Location
    queryset = uke_models.Location.objects.distinct()
    filter_class = services.UkeLocationsFilterService

    def _get_single_location_filter_class(self):
        return services.UkeLocationFilterService


class UkeLocationDetailView(LocationDetailView):
    model = uke_models.Location
    template_name = 'popups/location_uke.html'
    filter_class = services.UkeLocationFilterService

    def _get_location_objects(self):
        """
        Returns objects associated to the location,
        ie. base stations or UKE permissions
        """
        permissions = super(UkeLocationDetailView, self)._get_location_objects()
        permissions_by_network = {}
        # Group permissions by network
        for permission in permissions:
            if permission.network not in permissions_by_network:
                permissions_by_network[permission.network] = []
            permissions_by_network[permission.network].append(permission)

        location_objects = []
        for network in permissions_by_network.keys():
            supported = permissions.distinct().filter(operator__network=network). \
                values('standard', 'band').exclude(standard='?', band='?')
            location_objects.append({
                'network': network,
                'supported': supported,
                'permissions': permissions_by_network[network],
            })
        return location_objects


# #####################
# MAP UI ELEMENTS VIEWS
# #####################


class ControlPanelView(generic.TemplateView):
    template_name = 'map/panels/control.html'

    def get_context_data(self, **kwargs):
        context = super(ControlPanelView, self).get_context_data(**kwargs)
        context['networks'] = bts_models.Network.objects.all()
        context['standards'] = bts_models.Cell.STANDARDS
        context['bands'] = bts_models.Cell.BANDS
        context['bts_last_update_date'] = self._get_last_update_date(bts_models.BaseStation)
        context['uke_last_update_date'] = self._get_last_update_date(uke_models.Permission)
        return context

    def _get_last_update_date(self, model):
        vals = model.objects.values('date_updated').order_by('-date_updated')[:1]
        if vals:
            return vals[0]['date_updated']
        return None


class StatusPanelView(generic.TemplateView):
    template_name = 'map/panels/status.html'


class AdPanelView(generic.TemplateView):
    template_name = 'map/panels/googlead.html'
