from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from .map.api import LocationResource as MapLocationResource, UkeLocationResource
from . import views

# API to serve map-related requests
api_map = Api(api_name='map')
api_map.register(MapLocationResource())
api_map.register(UkeLocationResource())

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_map.urls)),
    url(r'^bts/', include('btsearch.bts.urls', namespace='bts')),
    url(r'^map/', include('btsearch.map.urls', namespace='map')),
    url(r'', views.IndexView.as_view(), name='index-view'),
)
