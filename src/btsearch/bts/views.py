from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import ListView, RedirectView
from btsearch.bts.models import BaseStation


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
        ctx['num_rows'] = self.get_queryset().count()
        if 'query' in self.kwargs:
            ctx['q'] = self.kwargs['query']
        return ctx

    def get_queryset(self):
        qs = super(BtsListingView, self).get_queryset()
        if 'query' in self.kwargs:
            query = self.kwargs['query']
            qs = qs.filter(Q(location__town__icontains=query) |
                           Q(location__address__icontains=query))

        return qs
