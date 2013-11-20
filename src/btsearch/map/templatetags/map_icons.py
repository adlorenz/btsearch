from django import template

from btsearch import services

register = template.Library()


@register.filter
def get_icon(object):
    map_icon_service = services.MapIconService()
    try:
        return map_icon_service.get_icon_by_network(object.network)
    except:
        return ''
