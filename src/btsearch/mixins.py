class QuerysetFilterMixin(object):

    filter_service = None

    def __init__(self):
        self.filter_service = self.filter_class()

    def get_queryset_filters(self):
        raw_filters = self.request.GET.copy()
        return self.filter_service.get_processed_filters(raw_filters)
