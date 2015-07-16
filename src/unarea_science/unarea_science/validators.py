from datetime import datetime
from unarea_core.lib.jsonscheme.parser import JSONParser
from unarea_core.lib.jsonscheme.validators import BsonObjectId, String, Boolean, Datetime, Nullable, NotEmpty, \
    DatetimeString

new_project_validator = JSONParser({
    u"+theme": String(min_length=1),
    u"is_thesis": NotEmpty(Boolean(), default=False),
    u"abstract": NotEmpty(String(min_length=50)),
    u"year_of_start": NotEmpty(DatetimeString(), default=datetime.utcnow()),
    u"performer_id": NotEmpty(BsonObjectId()),
    u"supervisor_id": NotEmpty(BsonObjectId())
})


update_project_validator = JSONParser({
    u"theme": Nullable(String(min_length=1)),
    u"is_thesis": Nullable(Boolean()),
    u"abstract": Nullable(String()),
    u"year_of_start": Nullable(DatetimeString()),
    u"performer_id": Nullable(BsonObjectId()),
    u"supervisor_id": Nullable(BsonObjectId())
})