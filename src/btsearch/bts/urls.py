from django.conf.urls.defaults import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^bts_details/(?P<pk>\d+)/$',
        views.BaseStationDetailView.as_view(),
        name='base-station-extended-info-view'),

    url(r'^uke_details/(?P<pk>\d+),(?P<network_code>\d+)/$',
        views.UkeLocationDetailView.as_view(),
        name='uke-location-extended-info-view'),

    url(r'',
        views.BtsListingView.as_view(),
        name='bts-listing')
)
