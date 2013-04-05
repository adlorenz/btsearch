from django.conf.urls.defaults import patterns, url
from btsearch.bts.views import BtsListingView, SearchRedirectView

urlpatterns = patterns(
    '',
    url(r'^/query/(?P<query>.*)/', BtsListingView.as_view(), name='bts-query'),
    url(r'^/search', SearchRedirectView.as_view(), name='bts-search'),
    url(r'', BtsListingView.as_view(), name='bts-listing')
)
