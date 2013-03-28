from tastypie import fields
from tastypie.resources import ModelResource
from btsearch.bts.models import BaseStation, Location, Cell, Network, Region

class RegionResource(ModelResource):
    class Meta:
        queryset = Region.objects.all()


class LocationResource(ModelResource):
    region = fields.ForeignKey(RegionResource, 'region', full=True)
    codes = fields.CharField(attribute='get_network_codes_for_map')
    
    class Meta:
        queryset = Location.objects.all()


class NetworkResource(ModelResource):
    class Meta:
        queryset = Network.objects.all()


class BaseStationResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location')
    network = fields.ForeignKey(NetworkResource, 'network', full=True)
    cells = fields.ToManyField('btsearch.bts.api.BaseStationCellsResource', 'cell_set', full=True)
    
    class Meta:
        queryset = BaseStation.objects.all()


class BaseStationCellsResource(ModelResource):
    date_ping = fields.DateTimeField(attribute='date_ping', null=True)
    
    class Meta:
        queryset = Cell.objects.all()
        resource_name = 'cells'
        excludes = ['base_station']


class CellResource(ModelResource):
    basestation = fields.ForeignKey(BaseStationResource, 'base_station')
    date_ping = fields.DateTimeField(attribute='date_ping', null=True)
    
    class Meta:
        queryset = Cell.objects.all()
