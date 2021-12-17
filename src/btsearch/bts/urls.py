from django.urls import path

from . import views

app_name = 'bts'

urlpatterns = [
    path('details/<int:pk>/',
        views.BtsDetailView.as_view(),
        name='bts-extended-info-view'),

    path('ukedetails/<int:pk>,<int:network_code>/',
        views.UkeDetailView.as_view(),
        name='uke-extended-info-view'),

    path('export/download/',
        views.ExportDownloadView.as_view(),
        name='export-download-view'),

    path('export/',
        views.ExportFilterView.as_view(),
        name='export-filter-view'),

    path('',
        views.BtsListingView.as_view(),
        name='listing')
]
