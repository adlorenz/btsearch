from django import template

register = template.Library()


@register.filter
def metadata(object):
    cell = object
    metadata = []
    metadata.append(cell.base_station.location.region.code)
    metadata.append(cell.base_station.station_id)
    if cell.standard == 'UMTS':
        metadata.append(cell.base_station.rnc)
    if cell.standard != '?':
        stdbnd = '{}{}'.format(cell.standard[0], cell.band)
        if cell.standard == 'UMTS':
            stdbnd += '-{}'.format(cell.ua_freq)
        metadata.append(stdbnd)
    return ':'.join([str(item) for item in metadata])
