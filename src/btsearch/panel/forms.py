# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory

from ..bts import models


class BaseStationEditForm(forms.ModelForm):

    class Meta:
        model = models.BaseStation
        widgets = {
            'location': forms.HiddenInput(),
        }

BaseStationCellsFormSet = inlineformset_factory(
    models.BaseStation,
    models.Cell,
    extra=1,
    can_delete=True,
    fields=('standard', 'band', 'ua_freq', 'lac', 'cid', 'cid_long', 'ecid',
            'is_confirmed', 'notes')
)
