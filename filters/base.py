class BaseFilter:
    def __init__(self, request):
        self.request = request
        self.filters = []

    def apply(self):
        for fil_ter in self.filters:
            if hasattr(self, fil_ter) and self.request.query_arguments.get(fil_ter): # noqa E501
                filter_method = getattr(self, fil_ter)  # Thank's @MrFedora
                result = filter_method(
                    self.request.query_arguments[fil_ter][0].decode())
        return result

    def done(self):
        return self.apply()
