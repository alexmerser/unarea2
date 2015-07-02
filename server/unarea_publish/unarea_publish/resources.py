from bson.objectid import ObjectId
from datetime import datetime

from unarea_core.mongodb.documents import BaseDocument
from unarea_core.mongodb.bins import MONGODB

class PostDocument(BaseDocument):
    collection_name = u'posts'
    database = MONGODB
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