from datetime import datetime
import uuid
from bson.objectid import ObjectId
from unarea_server.core.mongodb.documents import BaseDocument

class UserSessionDocument(BaseDocument):
    collection_name = u"user_sessions"

    structure = {
        u"user_id": ObjectId,
        u"token": unicode,
        u"is_api_token": bool,
        u"updated": datetime,
        u"data": dict,
    }

    required = [u"user_id", u"token"]

    @classmethod
    def get_hash(cls):
        return unicode(uuid.uuid4())
