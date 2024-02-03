# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from ..bts import models
from .. import services


class BaseStationEditForm(forms.ModelForm):
    class Meta:
        model = models.BaseStation
        widgets = {
            'location': forms.HiddenInput(),
        }
        fields = '__all__'


class LocationEditForm(forms.ModelForm):
    class Meta:
        model = models.Location
        widgets = {
            'location_hash': forms.HiddenInput(),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LocationEditForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs['maxlength'] = 9
        self.fields['longitude'].widget.attrs['maxlength'] = 9

    def clean(self):
        # Calculate location_hash
        lat = str(self.cleaned_data['latitude'])
        lng = str(self.cleaned_data['longitude'])
        self.cleaned_data['location_hash'] = \
            services.LocationHasherService(lat, lng).get()
        return self.cleaned_data


BaseStationCellsFormSet = inlineformset_factory(
    models.BaseStation,
    models.Cell,
    extra=1,
    can_delete=True,
    fields=('standard', 'band', 'ua_freq', 'lac', 'cid', 'cid_long',
            'is_confirmed', 'notes')
)
