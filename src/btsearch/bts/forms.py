from django import forms

from . import models


class ListingFilterForm(forms.Form):

    query = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    network = forms.ModelChoiceField(
        required=False,
        queryset=models.Network.objects.all()
    )

    region = forms.ModelChoiceField(
        required=False,
        queryset=models.Region.objects.all()
    )
