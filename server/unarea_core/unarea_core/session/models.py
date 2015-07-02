from datetime import datetime, timedelta
from pymongo.errors import DuplicateKeyError
from unarea_core.session.domains import Session

class SessionModel(object):
    def __init__(self, session_document, user_resource):
        self._session_resource = session_document
        self._user_resource = user_resource

    def new(self, user, is_api=False):
        """ Construct unique session for a given user """
        token = self._session_resource.get_hash()
        session = Session(user_id=user.user_id,
                          token=token,
                          created=datetime.utcnow(),
                          updated=datetime.utcnow(),
                          is_api_token=is_api)
        return session

    def is_valid(self, session):
        """
        Method check the validness of a session by a given token.
        Parameters:
        - session_object (object) - Session ID
        """

        if session.is_api_token:
            return True

        if not session.updated or (session.updated + timedelta(seconds=6000)) <= datetime.utcnow():
            self._session_resource.collection.remove(session.serialize())
            return False

        return True

    def create_session_for_user(self, user):
        """
        This method will create session for user and return it's token

        :param user: user to create session for
        :type user: User instance

        :return: new session's token
        :rtype: str
        """
        new_session = self.new(user)
        self._session_resource.collection.insert(new_session.serialize())
        return new_session

    def get_by_user(self, user, additional_query=None):
        """ List Session for a given user
        :param user:
        :param additional_query:
        """

        q = {"user_id": user.user_id}
        if additional_query:
            q.update(additional_query)
        res = self._session_resource.collection.find(q)
        for sdoc in res:
            session = Session(user_id=sdoc["user_id"],
                              token=sdoc["token"],
                              created=sdoc["created"],
                              updated=sdoc["updated"],
                              is_api_token=sdoc["is_api_token"],
                              session_id=sdoc["_id"])
            if not session.is_api_token and self.is_valid(session):
                return session

    def create(self, user):
        """ Construct mostly unique session for a given user """

        new_session = self.new(user)
        try:
            self._session_resource.collection.insert(new_session.serialize())
            return new_session
        except DuplicateKeyError:
            pass

    def create_service_session(self, user):
        """
        New session for a given user for inter service communication

        :param user: user
        :type user: UserDocument

        :return: SessionDocument
        :rtype: SessionDocument
        """

        session = self.new(user, is_api=True)
        self._session_resource.collection.insert(session.serialize())
        return session

    def flush(self, session_object):
        """ Remove Nimble session from both database and cache
         Method return None in all circumstances but can raise various exceptions.
         Parameters:
         - session_object (object) - session object
        """

        if session_object:
            self._session_resource.collection.remove({'_id': session_object.session_id})

    def get_by_token(self, session_token):
        """ Method return an Nimble session object or None.
        Parameters:
        - session_token (string) - Session ID
        """
        if not session_token:
            return None

        if not isinstance(session_token, basestring):
            return None
        res = self._session_resource.collection.find_one({"token": session_token})
        print res
        if not res:
            return None
        return Session(user_id=res["user_id"],
                       token=res["token"],
                       created=res["created"],
                       updated=res["updated"],
                       is_api_token=res["is_api_token"],
                       session_id=res["_id"])

    def delete_by_user_ids(self, user_ids):
        self._session_resource.collection.remove({'user_id': {'$in': user_ids}})

    def get_user_for_session(self, session):
        return self._user_resource.get_by_id(session.user_id)
