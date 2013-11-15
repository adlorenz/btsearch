from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^ukelocations/(?P<pk>\d+)/$',
        views.UkeLocationDetailView.as_view(),
        name='locations'),

    url(r'^ukelocations/$',
        views.UkeLocationsView.as_view(),
        name='locations'),

    url(r'^locations/(?P<pk>\d+)/$',
        views.LocationDetailView.as_view(),
        name='locations'),

    url(r'^locations/$',
        views.LocationsView.as_view(),
        name='locations'),

    url(r'^ui/control_panel/$',
        views.ControlPanelView.as_view(),
        name='control-panel-view'),

    url(r'^ui/status_panel/$',
        views.StatusPanelView.as_view(),
        name='status-panel-view'),

)
