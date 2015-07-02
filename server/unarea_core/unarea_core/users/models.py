from unarea_core.users.domains import User
import logging
log = logging.getLogger("unarea_auth.%s" % __name__)
class UserModel(object):
    def __init__(self, user_resource):
        self._user_resource = user_resource

    def get_by_id(self, user_id):
        res = self._user_resource.get_by_id(user_id)
        if res:
            user = User(
                first_name=res["first_name"],
                last_name=res["last_name"],
                email=res["email"],
                user_id=res["_id"]
            )
            return user

    def get(self, query):
        res = self._user_resource.collection.find_one(query)
        if res:
            user = User(
                first_name=res["first_name"],
                last_name=res["last_name"],
                email=res["email"],
                user_id=res["_id"]
            )
            return user

    def create(self, user, password):
        new_user = user.new_user()
        new_user.update({u"password": password})
        res = self._user_resource.collection.insert(new_user)
        return res

    def edit(self):
        pass

    def delete(self):
        pass