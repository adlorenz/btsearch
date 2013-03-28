from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from btsearch.bts.api import BaseStationResource, LocationResource, RegionResource, NetworkResource, CellResource
from btsearch.map.api import LocationResource as MapLocationResource, UkeLocationResource
from btsearch.map.views import BaseStationExtendedInfoView, ControlPanelView, IndexView, StatusPanelView, UkeLocationExtendedInfoView

api_v1 = Api(api_name='v1')
api_v1.register(LocationResource())
api_v1.register(BaseStationResource())
api_v1.register(RegionResource())
api_v1.register(NetworkResource())
api_v1.register(CellResource())

api_map = Api(api_name='map')
api_map.register(MapLocationResource())
api_map.register(UkeLocationResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_v1.urls)),
    url(r'^api/', include(api_map.urls)),
    url(r'^db', include('btsearch.bts.urls')),
    url(r'^get_control_panel/$', ControlPanelView.as_view(), name='control-panel-view'),
    url(r'^get_status_panel/$', StatusPanelView.as_view(), name='status-panel-view'),
    url(r'^get_base_station_info/(?P<pk>\d+)/$', BaseStationExtendedInfoView.as_view(), name='base-station-extended-info-view'),
    url(r'^get_uke_location_info/(?P<pk>\d+),(?P<network_code>\d+)/$', UkeLocationExtendedInfoView.as_view(), name='uke-location-extended-info-view'),
    url(r'', IndexView.as_view(), name='map-view'),
)
