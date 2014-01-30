from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from . import views


urlpatterns = patterns(
    '',
    url(r'^basestation/(?P<pk>\d+)$',
        staff_member_required(views.BaseStationView.as_view()),
        name='basestation-edit-view'),

    url(r'^basestation$',
        staff_member_required(views.BaseStationView.as_view()),
        name='basestation-add-view'),

    url(r'^location/(?P<pk>\d+)$',
        staff_member_required(views.LocationView.as_view()),
        name='location-edit-view'),

    url(r'^location$',
        staff_member_required(views.LocationView.as_view()),
        name='location-add-view'),

    url(r'^$',
        staff_member_required(views.IndexView.as_view()),
        name='index-view'),
)
