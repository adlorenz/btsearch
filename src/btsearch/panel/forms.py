# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from ..bts import models
from ..bts import widgets


class BaseStationEditForm(forms.ModelForm):

    location_info = forms.CharField(max_length=255, required=False)

    class Meta:
        model = models.BaseStation
        widgets = {
            'location': widgets.LocationSelectorWidget()
        }

    def __init__(self, *args, **kwargs):
        super(BaseStationEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            instance = kwargs['instance']
            self.initial['location_info'] = instance.location
            self.fields['location_info'].widget.attrs['readonly'] = True

BaseStationCellsFormSet = inlineformset_factory(
    models.BaseStation,
    models.Cell,
    extra=1,
    can_delete=True,
    fields=('standard', 'band', 'ua_freq', 'lac', 'cid', 'cid_long', 'ecid',
            'is_confirmed', 'notes')
)
