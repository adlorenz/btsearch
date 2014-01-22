# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from . import models
from . import widgets


class ListingFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    network = forms.ModelChoiceField(
        required=False,
        queryset=models.Network.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
        # empty_label='Sieć',
    )
    region = forms.ModelChoiceField(
        required=False,
        queryset=models.Region.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    standard = forms.MultipleChoiceField(
        required=False,
        choices=models.Cell.STANDARDS,
        widget=forms.CheckboxSelectMultiple(),
    )
    band = forms.MultipleChoiceField(
        required=False,
        choices=models.Cell.BANDS,
        widget=forms.CheckboxSelectMultiple(),
    )


class ExportFilterForm(forms.Form):

    FORMATS = (
        ('2.0', 'CLF v2.0'),
        ('2.1', 'CLF v2.1'),
        ('3.0d', 'CLF v3.0 (dec)'),
        ('3.0h', 'CLF v3.0 (hex)'),
        ('4.0', 'CLF v4.0'),
    )

    network = forms.ModelChoiceField(
        required=True,
        queryset=models.Network.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # network = forms.MultipleChoiceField(
    #     required=True,
    #     choices=((network.code, network) for network in models.Network.objects.all()),
    #     widget=forms.CheckboxSelectMultiple(),
    # )
    region = forms.MultipleChoiceField(
        required=True,
        choices=((region.id, region.name) for region in models.Region.objects.all()),
        widget=forms.CheckboxSelectMultiple(),
    )
    standard = forms.MultipleChoiceField(
        required=False,
        choices=models.Cell.STANDARDS,
        widget=forms.CheckboxSelectMultiple(),
    )
    band = forms.MultipleChoiceField(
        required=False,
        choices=models.Cell.BANDS,
        widget=forms.CheckboxSelectMultiple(),
    )
    output_format = forms.ChoiceField(
        required=True,
        choices=FORMATS,
        widget=forms.RadioSelect(),
        initial='3.0d'
    )


class BaseStationEditForm(forms.ModelForm):

    location_info = forms.CharField(max_length=255, required=False)

    class Meta:
        model = models.BaseStation
        widgets = {
            'location': widgets.LocationSelectorWidget()
        }

    def __init__(self, *args, **kwargs):
        super(BaseStationEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['location_info'] = instance.location
            self.fields['location_info'].widget.attrs['readonly'] = True

BaseStationCellsFormSet = inlineformset_factory(
    models.BaseStation, models.Cell, extra=1)
