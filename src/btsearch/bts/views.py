from django.db.models import Q
from django.views import generic

from . import models
from . import forms


class BtsListingView(generic.ListView):
    template_name = 'bts/listing.html'
    model = models.BaseStation
    queryset = models.BaseStation.objects.order_by('-date_updated')
    context_object_name = 'basestations'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super(BtsListingView, self).get_context_data(**kwargs)
        ctx['filter_form'] = forms.ListingFilterForm(self.request.GET)
        ctx['get_params'] = self.request.GET.copy()
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

        return qs
