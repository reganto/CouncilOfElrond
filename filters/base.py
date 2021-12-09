class BaseFilter:
    def __init__(self, upcoming_filters):
        self.upcoming_filters = upcoming_filters
        self.expected_filters = []

    def _apply(self):
        for _filter in self.expected_filters:
            if hasattr(self, _filter) and self.upcoming_filters.get(_filter): # noqa E501
                filter_method = getattr(self, _filter)  # Thank's @MrFedora 
                result = filter_method(
                    self.upcoming_filters[_filter][0].decode())
        return result

    def done(self):
        return self._apply()
