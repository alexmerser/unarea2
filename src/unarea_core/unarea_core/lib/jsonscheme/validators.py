import re
from bson.objectid import ObjectId, InvalidId
from dateutil.parser import parse

from valideer import ValidationError, Validator
from valideer.validators import *

class DatetimeString(Validator):
    """
    Custom validator, validating date string in any format and try to parse with it
    """
    name = u"date_time_str"

    def validate(self, value, adapt=True):
        if adapt:
            try:
                dtime = parse(value)
                return dtime
            except TypeError:
                raise ValidationError(u"Can not parse provided date-string!", value)
        else:
            return value

class EmailString(Pattern):
    """
    Validator for email
    """
    name = u"email"
    regexp = re.compile(r"^([-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
                        r'|^([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*'
                        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,30}\.?$', re.IGNORECASE)

    def __init__(self):
        super(EmailString, self).__init__()


class BsonObjectId(String):
    """
    Custom validator, validation BSON ObjectId and convert it
    """
    name = u"object_id"

    def __init__(self):
        super(BsonObjectId, self).__init__()

    def validate(self, value, adapt=True):
        super(BsonObjectId, self).validate(value)
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError(u"invalid object id {}".format(value), value)


class NotEmpty(Nullable):
    """
    If some value declared as NotEmpty, it will be always present in resulting dict, even if it wasn't present
    in the incoming dictionary
    """

    @property
    def default_object_property(self):
        return self.default
