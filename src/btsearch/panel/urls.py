from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required

from . import views


urlpatterns = patterns(
    '',
    url(r'^basestation/(?P<pk>\d+)$',
        staff_member_required(views.BaseStationPanelView.as_view()),
        name='basestation-edit-view'),

    url(r'^basestation$',
        staff_member_required(views.BaseStationPanelView.as_view()),
        name='basestation-add-view'),
)
