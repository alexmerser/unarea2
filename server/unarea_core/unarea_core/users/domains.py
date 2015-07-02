class User(object):
    def __init__(self, first_name, last_name, email, user_id=None):
        """
        Domain level user object

        :param user_id:
        :param first_name:
        :param last_name:
        :param email:
        """

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def new_user(self):
        return {
            u"first_name": self.first_name,
            u"last_name": self.last_name,
            u"email": self.email,
        }

    def serialize(self):
        return {
            u"first_name": self.first_name,
            u"last_name": self.last_name,
            u"email": self.email,
        }