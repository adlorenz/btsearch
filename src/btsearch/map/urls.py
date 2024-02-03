from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('ukelocations/<int:pk>/',
        views.UkeLocationDetailView.as_view(),
        name='locations'),

    path('ukelocations/',
        views.UkeLocationsView.as_view(),
        name='locations'),

    path('locations/<int:pk>/',
        views.LocationDetailView.as_view(),
        name='locations'),

    path('locations/',
        views.LocationsView.as_view(),
        name='locations'),

    path('ui/control_panel/',
        views.ControlPanelView.as_view(),
        name='control-panel-view'),

    path('ui/status_panel/',
        views.StatusPanelView.as_view(),
        name='status-panel-view'),

    path('ui/ad_panel/',
        views.AdPanelView.as_view(),
        name='ad-panel-view'),
]
