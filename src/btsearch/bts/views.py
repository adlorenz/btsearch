from django.views.generic import TemplateView, ListView, RedirectView
from django.db.models import Q
from btsearch.bts.models import BaseStation
from django.core.urlresolvers import reverse

class IndexView(TemplateView):
    template_name = 'bts/index.html'
    
class SearchRedirectView(RedirectView):
    def get_redirect_url(self):
        return reverse('bts-query', kwargs={'query': self.request.GET['search']})
    
class BtsListingView(ListView):
    template_name = 'bts/listing.html'
    model = BaseStation
    queryset = BaseStation.objects.all()
    context_object_name = 'basestations'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(BtsListingView, self).get_context_data(**kwargs)
        if 'query' in self.kwargs:
            context['q'] = self.kwargs['query']
        return context

    def get_queryset(self):
        qs = super(BtsListingView, self).get_queryset()
        if 'query' in self.kwargs:
            query = self.kwargs['query']
            qs = qs.filter(Q(location__town__icontains=query) |
                           Q(location__address__icontains=query))
            
        return qs