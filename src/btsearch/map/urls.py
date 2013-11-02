from django.conf.urls.defaults import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^bts_locations/',
        views.BtsLocationsView.as_view(),
        name='bts-locations'),
    url(r'^ui/control_panel/$',
        views.ControlPanelView.as_view(),
        name='control-panel-view'),
    url(r'^ui/status_panel/$',
        views.StatusPanelView.as_view(),
        name='status-panel-view'),

)
