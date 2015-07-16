from flask_security import UserMixin, RoleMixin

from unarea_core.db import DynamicDocument, Document
from unarea_core.db.fields import String, Email, Boolean, DateTime,\
    List, ObjectId, URL

class Role(Document, RoleMixin):
    name = String(max_length=80, unique=True)
    description = String(max_length=255)

    def __unicode__(self):
        return u"<Role {} <name='{}'>".format(self.id, self.name)


class User(DynamicDocument, UserMixin):
    username = String(max_length=50, required=False, unique=True)
    email = Email(max_length=255, unique=True)
    password = String(max_length=255)
    active = Boolean(default=True)
    confirmed_at = DateTime()
    last_login_at = DateTime()
    current_login_at = DateTime()
    last_login_ip = String(max_length=255)
    current_login_ip = String(max_length=255)

    auth_token = String(max_length=255)
    remember = Boolean(default=True)
    token_expired_date = DateTime()
    roles = List()


class UserAccount(Document):
    user_id = ObjectId()
    full_name = String(max_length=255)
    birthday = DateTime()
    address = String(max_length=255)
    skype = String(max_length=255)
    site = URL(max_length=255)