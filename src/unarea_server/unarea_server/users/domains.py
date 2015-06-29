class User(object):
    def __init__(self, first_name, last_name, email, is_active, user_id=None):
        """
        Domain level user object

        :param user_id:
        :param first_name:
        :param last_name:
        :param email:
        :param is_active:
        """

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = is_active

    def new_user(self):
        return {
            u"first_name": self.first_name,
            u"last_name": self.last_name,
            u"email": self.email,
            u"is_active": False
        }

    def serialize(self):
        return {
            u"first_name": self.first_name,
            u"last_name": self.last_name,
            u"email": self.email,
            u"is_active": False
        }