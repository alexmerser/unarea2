from unarea_core.lib.jsonscheme.parser import JSONParser
from unarea_core.lib.jsonscheme.validators import EmailString
from valideer import String

new_user_validator = JSONParser({
    u"+email": EmailString(),
    u"+password": String(min_length=1),
    u"username": String(min_length=1),

})

login_user_validator = JSONParser({
    u"+email": EmailString(),
    u"+password": String(min_length=1),
})
