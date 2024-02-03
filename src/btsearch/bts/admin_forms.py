from django import forms

from . import models
from . import widgets


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = models.Location
        widgets = {
            'town': widgets.LocationPickerWidget()
        }
        fields = '__all__'


class BaseStationAdminForm(forms.ModelForm):

    class Meta:
        model = models.BaseStation
        widgets = {
            'location': widgets.LocationSelectorWidget()
        }
        fields = '__all__'

    location_info = forms.CharField(max_length=255, required=False)
    location_coords = forms.CharField(max_length=255, required=False)
    location_selected = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(BaseStationAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['location_info'] = instance.location
            self.fields['location_info'].widget.attrs['readonly'] = True
            self.fields['location_selected'].widget.attrs['readonly'] = True
            self.initial['location_coords'] = instance.location_coords
