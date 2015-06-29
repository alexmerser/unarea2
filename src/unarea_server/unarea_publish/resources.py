from bson.objectid import ObjectId
from datetime import datetime

from unarea_server.core.mongodb.documents import BaseDocument

class PostDocument(BaseDocument):
    collection_name = u'posts'

    structure = {
        u'title': unicode,
        u'owner_id': ObjectId,
        u'body': unicode,  # TODO: MARKUP SAFE
        u'is_approved': bool,
        u'created': datetime,
        u'updated': datetime,
        u'tags': list
    }

    shortcuts = {}