from django.conf.urls.defaults import patterns, url
from btsearch.bts.views import IndexView, BtsListingView, SearchRedirectView

urlpatterns = patterns('',
    url(r'^/query/(?P<query>.*)/', BtsListingView.as_view(), name='bts-query'),
    url(r'^/search', SearchRedirectView.as_view(), name='bts-search'),
    url(r'^/list', BtsListingView.as_view(), name='bts-listing'),
    url(r'', IndexView.as_view(), name='bts-index')
)