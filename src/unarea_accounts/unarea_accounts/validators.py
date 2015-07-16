from unarea_core.lib.jsonscheme.parser import JSONParser
from unarea_core.lib.jsonscheme.validators import EmailString, DatetimeString
from valideer import String

new_user_validator = JSONParser({
    u"+email": EmailString(),
    u"+password": String(min_length=5),
    u"+confirm": String(min_length=5),
    u"+full_name": String(min_length=5),
    u"+birth_day": DatetimeString()
})

login_user_validator = JSONParser({
    u"+email": EmailString(),
    u"+password": String(min_length=1),
})
