from datetime import datetime
import pymongo
from bson.objectid import ObjectId


class UserSessionModel(object):

    def __init__(self, document):
        self.document = document()

    def get_by_user(self, user, additional_query=None):
        """ List NimbleSession for a given user """

        document_class = self.document

        q = {"user_id": user['_id']}
        if additional_query:
            q.update(additional_query)

        return document_class.find(q)

    def create(self, user):
        """ Construct mostly unique NimbleSession for a given user """

        while True:
            token = self.document.get_hash()

            try:
                rv = self.document()
                rv["user_id"] = user["_id"]
                rv._user = user
                rv["token"] = token
                rv["updated"] = datetime.utcnow()
                rv.save()

                return rv
            except:
                pass

    def flush(self, session_object):
        """ Remove Nimble session from both database and cache
         Method return None in all circumstances but can raise various exceptions.
         Parameters:
         - session_object (object) - NimbleSession object
        """
        if session_object:
            self.document.remove({'_id': session_object['_id']})

    def get_by_token(self, session_token):
        """ Method return an Nimble session object or None.
        Parameters:
        - session_token (string) - Session ID
        """
        if not session_token:
            return None

        if not isinstance(session_token, basestring):
            return None

        rv = self.document.find_one({"token": session_token})
        if not rv:
            return None
        return self.document(doc=rv)

    def is_valid(self, session_object):
        """
        Method check the validness of a session by a given token.
        Parameters:
        - session_object (object) - Session ID
        """
        if not session_object["updated"] or (session_object["updated"] + timedelta(seconds=86400)) <= datetime.utcnow():
            self.flush(session_object)
            return False

        return True

    def get_last_session_for_user(self, user_id):
        """
        Get last session for for user

        :param user_id: user ID
        :type user_id: bson.objectid.ObjectId

        :return: NimbleSessionDocument or None
        :rtype: NimbleSessionDocument or None
        """
        assert isinstance(user_id, ObjectId)

        try:
            return self.document.find({"user_id": user_id, "is_api_token": False}).sort(
                [("updated", pymongo.DESCENDING)]).next()
        except StopIteration:
            return None

    @staticmethod
    def update_session(session_object):
        """
        Method refreshed Nimble session. Returns True or False.
        Parameters:
        - session_object (object) - NimbleSession object
        """

        _now = datetime.utcnow()
        if session_object["updated"] + timedelta(seconds=120) <= _now:
            session_object["updated"] = _now
            session_object.save()

        return True

    def delete_by_user_ids(self, user_ids):
        self.document.remove({'user_id': {'$in': user_ids}})