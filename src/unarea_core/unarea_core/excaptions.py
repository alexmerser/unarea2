class NotFoundError(Exception):
    def __init__(self, class_obj, project_id, **kwargs):
        self._project_id = project_id
        self.message = u"%s with id %s not exists!" % (class_obj.__name__, self._project_id)
        super(NotFoundError, self).__init__(**kwargs)