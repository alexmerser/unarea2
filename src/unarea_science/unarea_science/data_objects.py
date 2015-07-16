from flask_restful import fields

from unarea_core.db import Document
from unarea_core.db.fields import String, Boolean, ObjectId, DateTime
import datetime

class DateTimeField(fields.Raw):
    def __init__(self, **kwargs):
        super(DateTimeField, self).__init__(**kwargs)

    def format(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S%z")

class ScienceProjects(Document):
    supervisor_id = ObjectId()
    performer_id = ObjectId()
    theme = String(max_length=200, required=True)
    abstract = String()
    is_thesis = Boolean()
    year_of_start = DateTime(default=datetime.datetime.utcnow())
    is_closed = Boolean(default=False)
    created = DateTime(default=datetime.datetime.utcnow())
    updated = DateTime(default=datetime.datetime.utcnow())

    @property
    def json_dict(self):
        return {
            u"id": unicode(self.id),
            u"supervisor": unicode(self.supervisor_id),
            u"performer": unicode(self.performer_id),
            u"theme": self.theme,
            u"abstract": self.abstract,
            u"is_thesis": self.is_thesis
        }

    @classmethod
    def json_fields(cls):
        return {
            u"id": fields.String,
            u"supervisor": fields.String,
            u"performer": fields.String,
            u"theme": fields.String,
            u"abstract": fields.String,
            u"is_thesis": fields.Boolean,
            u"year_of_start": DateTimeField,
            u"created": DateTimeField,
            u"updated": DateTimeField,

        }
