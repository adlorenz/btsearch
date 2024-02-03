from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'panel'

urlpatterns = [
    path('basestation/<int:pk>/',
        staff_member_required(views.BaseStationView.as_view()),
        name='basestation-edit-view'),

    path('basestation/',
        staff_member_required(views.BaseStationView.as_view()),
        name='basestation-add-view'),

    path('location/<int:pk>/',
        staff_member_required(views.LocationView.as_view()),
        name='location-edit-view'),

    path('location/',
        staff_member_required(views.LocationView.as_view()),
        name='location-add-view'),

    path('',
        staff_member_required(views.IndexView.as_view()),
        name='index-view'),
]
