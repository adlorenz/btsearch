from django.conf import settings


def metadata(request):
    """
    Inspired by django-oscar, see:
    https://github.com/tangentlabs/django-oscar/blob/5642461b61feef2a2e93c6a7de34061ad7d66ed4/oscar/core/context_processors.py
    """
    return {
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'version': getattr(settings, 'VERSION', None),
        'googlemaps_apikey': getattr(settings, 'GOOGLEMAPS_APIKEY', None)
    }
