from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^btsadmin/', include(admin.site.urls)),
    url(r'^bts/', include('btsearch.bts.urls', namespace='bts')),
    url(r'^map/', include('btsearch.map.urls', namespace='map')),
    url(r'^$', views.IndexView.as_view(), name='home'),
)
