from django.forms import ModelForm, CharField
from btsearch.bts.models import BaseStation, Location
from btsearch.bts.widgets import LocationPickerWidget, LocationSelectorWidget

class LocationAdminForm(ModelForm):
    class Meta:
        model = Location
        widgets = {
            'town': LocationPickerWidget()
        }
        
class BaseStationAdminForm(ModelForm):
    class Meta:
        model = BaseStation
        widgets = {
            'location': LocationSelectorWidget()
        }
        
    location_info = CharField(max_length=255, required=False)
    location_coords = CharField(max_length=255, required=False)
    location_selected = CharField(max_length=255, required=False)
    
    def __init__(self, *args, **kwargs):
        super(BaseStationAdminForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['location_info'] = instance.location
            self.fields['location_info'].widget.attrs['readonly'] = True
            self.fields['location_selected'].widget.attrs['readonly'] = True
            self.initial['location_coords'] = instance.location_coords