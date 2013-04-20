from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import ListView, RedirectView
from btsearch.bts.models import BaseStation, Network, Cell


class SearchRedirectView(RedirectView):

    def get_redirect_url(self):
        search_query = self.request.GET.get('search', None)
        if search_query:
            return reverse('bts-query', kwargs={'query': search_query})
        else:
            return reverse('bts-listing')


class BtsListingView(ListView):
    template_name = 'bts/listing.html'
    model = BaseStation
    queryset = BaseStation.objects.order_by('-date_updated')
    context_object_name = 'basestations'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super(BtsListingView, self).get_context_data(**kwargs)
        if 'query' in self.kwargs:
            ctx['q'] = self.kwargs['query']

        ctx['networks'] = Network.objects.all()
        ctx['standards'] = Cell.STANDARDS
        ctx['bands'] = Cell.BANDS
        # ctx['num_rows'] = self.get_queryset().count()
        return ctx

    def get_queryset(self):
        qs = super(BtsListingView, self).get_queryset()
        if 'query' in self.kwargs:
            query = self.kwargs['query']
            qs = qs.filter(Q(location__town__icontains=query) |
                           Q(location__address__icontains=query) |
                           Q(station_id=query))

        filters = dict(self.request.GET)
        if 'network' in filters and int(filters['network'][0]) > -1:
            qs = qs.filter(network__code=filters['network'][0])

        if 'standard' in filters and 'band' in filters:
            qs = qs.filter(cell__standard__in=list(filters['standard']),
                           cell__band__in=list(filters['band']))
        elif 'standard' in filters:
            qs = qs.filter(cell__standard__in=list(filters['standard']))
        elif 'band' in filters:
            qs = qs.filter(cell__band__in=list(filters['band']))

        return qs
