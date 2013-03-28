from django import forms
from django.conf import settings

class LocationPickerWidget(forms.TextInput):
    """
    Widget to pick a location from Google Map in Location admin view
    """
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'css/admin.forms.css',
            )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
            settings.STATIC_URL + 'js/admin.locationpicker.js',
        )
        
class LocationSelectorWidget(forms.TextInput):
    """
    Widget to select an exisitng Location from Google Map in BaseStation admin view
    """
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'css/admin.forms.css',
            )
        }
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
            settings.STATIC_URL + 'js/admin.locationselector.js',
        )