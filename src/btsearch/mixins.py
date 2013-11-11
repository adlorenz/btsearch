from . import services


class QuerysetFilterMixin(object):

    network_filter_field = None
    standard_filter_field = None
    band_filter_field = None
    region_filter_field = None

    def get_queryset_filters(self):
        filter_service = services.QuerysetFilterService(
            network_filter_field=self.network_filter_field,
            standard_filter_field=self.standard_filter_field,
            band_filter_field=self.band_filter_field,
            region_filter_field=self.region_filter_field,
        )
        raw_filters = self.request.GET.copy()
        return filter_service.get_processed_filters(raw_filters)
