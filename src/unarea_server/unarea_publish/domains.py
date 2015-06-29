class Post(object):
    def __init__(self, title, owner_id, body, is_approved, created, updated, tags):
        self.title = title
        self.owner_id = owner_id
        self.body = body
        self.is_approved = is_approved
        self.created = created
        self.updated = updated
        self.tags = tags

    def serialize(self):
        return {
            u'title': self.title,
            u'owner_id': self.owner_id,
            u'body': self.body,
            u'is_approved': self.is_approved,
            u'created': self.created,
            u'updated': self.updated,
            u'tags': self.tags
        }
