class UnauthorizedError(Exception):
    def __init__(self, **kwargs):
        self.message = u"Unauthorized request!"
        super(UnauthorizedError, self).__init__(**kwargs)
