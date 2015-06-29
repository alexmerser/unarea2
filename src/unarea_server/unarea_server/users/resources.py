from unarea_server.core.db.documents import BaseDocument


class UserDocument(BaseDocument):

    collection_name = u'users'

    structure = {
        u'first_name': unicode,
        u'last_name': unicode,
        u'email': unicode,  # TODO: create mongo field EmailField
        u'password': unicode,  # TODO: create mongo PasswordField
        u'is_active': bool,
    }
    # TODO: think about AUTO shortcuts creation, with user_shortcuts option to avoid duplicate names
    shortcuts = {
        u'first_name': u'fn',
        u'last_name': u'ln',
        u'email': u'e',
        u'password': u'p',
        u'is_active': u'iac',
    }

    # TODO: validate required fields on create document
    required = [u'email', u'password']