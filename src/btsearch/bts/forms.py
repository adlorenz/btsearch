# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models


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
    network = forms.ModelChoiceField(
        required=True,
        queryset=models.Network.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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
