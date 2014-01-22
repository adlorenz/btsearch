from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = patterns(
    '',
    url(r'^details/(?P<pk>\d+)/$',
        views.BtsDetailView.as_view(),
        name='bts-extended-info-view'),

    url(r'^ukedetails/(?P<pk>\d+),(?P<network_code>\d+)/$',
        views.UkeDetailView.as_view(),
        name='uke-extended-info-view'),

    url(r'^export/download$',
        views.ExportDownloadView.as_view(),
        name='export-download-view'),

    url(r'^export',
        views.ExportFilterView.as_view(),
        name='export-filter-view'),

    url(r'^panel/(?P<pk>\d+)$',
        staff_member_required(views.BaseStationPanelView.as_view()),
        name='panel-details-view'),

    url(r'^panel$',
        staff_member_required(views.BaseStationPanelView.as_view()),
        name='panel-view'),

    url(r'^$',
        views.BtsListingView.as_view(),
        name='listing')
)
