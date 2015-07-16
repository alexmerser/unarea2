from flask_security import UserMixin, RoleMixin
from flask_restful import fields

from unarea_core.db import DynamicDocument, Document
from unarea_core.db.fields import String, Email, Boolean, DateTime,\
    List, ObjectId, URL

class DateTimeField(fields.Raw):
    def __init__(self, **kwargs):
        super(DateTimeField, self).__init__(**kwargs)

    def format(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S%z")

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

    @classmethod
    def json_fields(cls):
        return {
            u"id": fields.String,
            u"email": fields.String,
            u"active": fields.Boolean,
            u"confirmed_at": DateTimeField,
            u"last_login_at": DateTimeField,
            u"current_login_at": DateTimeField,
            u"last_login_ip": DateTimeField,
            u"current_login_ip": DateTimeField,
            u"roles": fields.List(fields.Nested(Role))}



class UserAccount(Document):
    user_id = ObjectId()
    full_name = String(max_length=255)
    birth_day = DateTime()
    address = String(max_length=255)
    skype = String(max_length=255)
    site = URL(max_length=255)

    @classmethod
    def json_fields(cls):
        return {
            u"user_id": fields.String,
            u"full_name": fields.String,
            u"birth_day": DateTimeField,
            u"address": fields.String,
            u"skype": fields.String,
            u"site": fields.String}