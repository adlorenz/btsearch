from django import template
from btsearch.map.utils import MapIconFactory

register = template.Library()


@register.filter
def get_icon(object):
    map_icon_factory = MapIconFactory()
    try:
        icon = map_icon_factory.get_icon_by_network(object.network)
        return map_icon_factory.get_icon_path(icon)
    except:
        return ''
