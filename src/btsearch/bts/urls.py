from django.conf.urls.defaults import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^details/(?P<pk>\d+)/$',
        views.BtsDetailView.as_view(),
        name='bts-extended-info-view'),

    url(r'^ukedetails/(?P<pk>\d+),(?P<network_code>\d+)/$',
        views.UkeDetailView.as_view(),
        name='uke-extended-info-view'),

    url(r'',
        views.BtsListingView.as_view(),
        name='listing')
)
