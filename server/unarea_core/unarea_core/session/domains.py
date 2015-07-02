class Session(object):
    def __init__(self, user_id, token, created, updated, is_api_token=False, session_id=None):
        self.session_id = session_id
        self.user_id = user_id
        self.token = token
        self.created = created
        self.updated = updated
        self.is_api_token = is_api_token

    def serialize(self):
        serialized = {
            u"user_id": unicode(self.user_id),
            u"token": self.token,
            u"created": self.created.strftime("%Y-%m-%dT%H:%M:%S"),
            u"updated": self.updated.strftime("%Y-%m-%dT%H:%M:%S"),
            u"is_api_token": self.is_api_token,
        }
        if self.session_id:
            serialized.update({u"session_id": unicode(self.session_id)})
        return serialized
