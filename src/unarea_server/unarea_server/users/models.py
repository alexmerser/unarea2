from unarea_server.users.resources import UserDocument
from unarea_server.users.domains import User

class UserModel(object):
    # TODO: should we move data_resource to base class as class property ?
    _data_resource = UserDocument()

    # TODO: use query dict for now
    def get(self, query):
        res = self._data_resource.find_one(query)
        if res[0]:
            user = User(
                res[0]["_id"],
                res[0]["first_name"],
                res[0]["last_name"],
                res[0]["email"],
                res[0]["is_active"]
            )
            return user

    def create(self, user, password):
        new_user = user.new_user()
        new_user.update({u"password": password})
        res = self._data_resource.insert(new_user)
        return res

    def edit(self):
        pass

    def delete(self):
        pass