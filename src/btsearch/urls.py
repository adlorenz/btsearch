from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
#from btsearch.bts.api import BaseStationResource, LocationResource, RegionResource, NetworkResource, CellResource
from btsearch.map.api import LocationResource as MapLocationResource, UkeLocationResource
from btsearch.map.views import ControlPanelView, IndexView, StatusPanelView

# API won't be used for time being
# api_v1 = Api(api_name='v1')
# api_v1.register(LocationResource())
# api_v1.register(BaseStationResource())
# api_v1.register(RegionResource())
# api_v1.register(NetworkResource())
# api_v1.register(CellResource())

# API to serve map-related requests
api_map = Api(api_name='map')
api_map.register(MapLocationResource())
api_map.register(UkeLocationResource())

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/', include(api_v1.urls)),
    url(r'^api/', include(api_map.urls)),
    url(r'^bts/', include('btsearch.bts.urls')),
    url(r'^get_control_panel/$', ControlPanelView.as_view(), name='control-panel-view'),
    url(r'^get_status_panel/$', StatusPanelView.as_view(), name='status-panel-view'),

    url(r'', IndexView.as_view(), name='map-view'),
)
