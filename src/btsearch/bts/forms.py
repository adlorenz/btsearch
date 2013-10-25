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
        # empty_label='Sieć',
    )
    region = forms.ModelChoiceField(
        required=False,
        queryset=models.Region.objects.all(),
        # empty_label='Województwo',
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
