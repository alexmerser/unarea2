from factory import Factory
import uuid
from datetime import datetime
from bson.objectid import ObjectId
from unarea_core.session.domains import Session

class SessionFactory(Factory):
    class Meta:
        model = Session
        inline_args = ('user_id',
                       'token',
                       'created',
                       'updated',
                       'is_api_token',
                       'session_id')
    user_id = ObjectId()
    token = unicode(uuid.uuid4())
    created = datetime.utcnow()
    updated = datetime.utcnow()
    is_api_token = False
    session_id = ObjectId()
