from django import template

register = template.Library()


@register.filter
def metadata(object):
    # [{{ cell.base_station.station_id}}:{{ cell.base_station.rnc }}:{% if cell.standard != '?' %}{{ cell.standard|first }}{{ cell.band }}{% endif %}{% if cell.standard == 'UMTS' %}-{{ cell.ua_freq }}{% endif %}]
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
    return ':'.join(map(lambda x: str(x), metadata))
