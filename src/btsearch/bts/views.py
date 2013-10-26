from django.db.models import Q
from django.views import generic

from ..uke import models as uke_models
from . import models
from . import forms


class BtsListingView(generic.ListView):
    template_name = 'bts/listing.html'
    model = models.BaseStation
    context_object_name = 'base_stations'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super(BtsListingView, self).get_context_data(**kwargs)
        ctx['filter_form'] = forms.ListingFilterForm(self.request.GET)
        ctx['get_params'] = self.request.GET.copy()
        ctx['rows_found'] = self.get_queryset().count()
        return ctx

    def get_queryset(self):
        filters = self.request.GET.copy()
        qs = super(BtsListingView, self).get_queryset()

        if filters.get('query'):
            query = filters.get('query')
            qs = qs.filter(
                Q(location__town__icontains=query) |
                Q(location__address__icontains=query) |
                Q(station_id=query)
            )

        if filters.get('network'):
            qs = qs.filter(network__code=filters.get('network'))

        if filters.get('region'):
            qs = qs.filter(location__region=filters.get('region'))

        if filters.getlist('standard'):
            qs = qs.filter(cell__standard__in=filters.getlist('standard'))

        if filters.getlist('band'):
            qs = qs.filter(cell__band__in=filters.getlist('band'))

        qs.order_by('-date_updated')

        return qs


class BaseStationDetailView(generic.DetailView):
    model = models.BaseStation
    context_object_name = 'base_station'
    template_name = 'bts/bts_details.html'


class UkeLocationDetailView(generic.DetailView):
    """
    Does UKE-specific view belong here?
    """
    model = uke_models.UkeLocation
    context_object_name = 'uke_location'
    template_name = 'map/uke_details.html'

    def get_context_data(self, **kwargs):
        try:
            network = models.Network.objects.get(code=self.kwargs.get('network_code'))
            ctx = super(UkeLocationDetailView, self).get_context_data(**kwargs)
            ctx['permissions'] = models.UkePermission.objects.filter(
                uke_location=self.object,
                network=network
            )
            ctx['network'] = network
        except:
            pass
        return ctx
