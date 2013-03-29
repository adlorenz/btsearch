from django import template
from btsearch.map.utils import MapIconFactory

register = template.Library()


@register.filter
def get_icon(object):
    icon_factory = MapIconFactory()
    try:
        return icon_factory.get_icon_by_network(object.network)
    except:
        return ''
