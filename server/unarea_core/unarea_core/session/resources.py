import uuid
from bson.objectid import ObjectId
from datetime import datetime
from unarea_core.mongodb.bins import MONGODB

from unarea_core.mongodb.documents import BaseDocument

class SessionDocument(BaseDocument):
    collection_name = u"unarea_sessions"
    database = MONGODB
    structure = {
        u"user_id": ObjectId,
        u"token": unicode,
        u"is_api_token": bool,
        u"created": datetime,
        u"updated": datetime,
        u"data": dict,
    }

    shortcuts = {
    }

    required = [u"user_id", u"token"]

    @classmethod
    def get_hash(cls):
        return unicode(uuid.uuid4())
