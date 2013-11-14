from django.db.models import Q
from django.views import generic

from ..uke import models as uke_models
from .. import mixins
from . import models
from . import forms


class BtsListingView(mixins.QuerysetFilterMixin, generic.ListView):
    template_name = 'bts/listing.html'
    model = models.BaseStation
    queryset = models.BaseStation.objects.distinct()
    context_object_name = 'base_stations'
    paginate_by = 20

    network_filter_field = 'network__code'
    standard_filter_field = 'cells__standard__in'
    band_filter_field = 'cells__band__in'
    region_filter_field = 'location__region'
    timedelta_filter_field = 'date_updated__gte'

    def get_context_data(self, **kwargs):
        ctx = super(BtsListingView, self).get_context_data(**kwargs)
        ctx['filter_form'] = forms.ListingFilterForm(self.request.GET)
        ctx['get_params'] = self.request.GET.copy()
        # ctx['rows_found'] = self.get_queryset().count()
        return ctx

    def get_queryset(self):
        qs = super(BtsListingView, self).get_queryset()

        filters = self.request.GET.copy()
        if filters.get('query'):
            query = filters.get('query')
            qs = qs.filter(
                Q(location__town__icontains=query) |
                Q(location__address__icontains=query) |
                Q(station_id=query)
            )

        qs_filters = self.get_queryset_filters()
        qs = qs.filter(**qs_filters)
        qs = qs.order_by('-date_updated')
        return qs


class BtsDetailView(generic.DetailView):
    model = models.BaseStation
    context_object_name = 'base_station'
    template_name = 'bts/details_bts.html'


class UkeDetailView(generic.DetailView):
    """
    Does UKE-specific view belong here?
    """
    model = uke_models.Location
    context_object_name = 'uke_location'
    template_name = 'bts/details_uke.html'

    def get_context_data(self, **kwargs):
        try:
            network = models.Network.objects.get(code=self.kwargs.get('network_code'))
            ctx = super(UkeDetailView, self).get_context_data(**kwargs)
            ctx['permissions'] = uke_models.Permission.objects.filter(
                location=self.object,
                operator__network=network
            )
            ctx['network'] = network
        except:
            pass
        return ctx
