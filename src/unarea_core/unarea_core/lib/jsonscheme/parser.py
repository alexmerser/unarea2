import sys
import json
import collections
from valideer import Validator, Object, ValidationError, parse


class JSONParserError(ValueError):
    def __init__(self, message, value=None, errors=None):
        super(JSONParserError, self).__init__(message, value, errors)
        self._errors = errors
        self.value = value

    @property
    def message(self):
        return self.args[0]

    @property
    def errors(self):
        return self._errors or {}


class JSONParser(Validator):
    def __init__(self, json_schema, converter=None, additional_properties=None):
        """
        Base json validator and parser
        Parse method returns dictionary, fully processed with given validator and populated with extra parameters
        If adapter callable is passed, it will be called to adapt given data. If adaprer is type, this class will
        try to create instance, using parsed dict values as arguments

        :param json_schema: validator, used to parse provided data. Can be specified either by valideer schema,
        that will be parsed automatically or by valideer's Validator instance itself.
        :type json_schema: collections.Mapping | Validator

        :param additional_properties: flag indicating how additional properties not specified by provided schema must
         be treated. True will leave them in resulting parsed data, False will reject them by throwing exception and
         None (default) will ignore them and remove from parsing results.
        :type additional_properties: bool | None

        :param converter: callable that will be used to cast value after adaptation, if None - will return dict with
         adapted data. Exact way how it will be called depends on nature of `validator` argument. If it's valideer
         schema or `valideer.Object` instance then `adapter` will be called with parsed data passed as **kwargs. For
         every other type of `validator` parsed data will be passed to `adapter` as a single argument. Such flexibility
         enables use of ValideerJSONParser both for JSON objects and single values.
        :type converter: func|type|None
        """
        super(JSONParser, self).__init__()
        if isinstance(json_schema, collections.Mapping):
            if additional_properties is None:
                additional_properties = Object.REMOVE
            json_schema = parse(json_schema, additional_properties=additional_properties)
        self._schema_validator = json_schema
        self._converter = converter

    def validate(self, value, adapt=True):
        parsed = self._schema_validator.validate(value, adapt)
        if adapt and self._converter is not None:
            return self._convert(parsed)
        else:
            return parsed

    def _decode_data(self, data):
        """
        Decode data, by loading it from JSON if necessary

        :param data: data from request

        :return: dictionary with processed data
        :rtype: dict

        :raises JSONParserError: if data is in unknown format
        """
        if isinstance(data, str):
            try:
                data = data.decode(u"utf-8")
            except UnicodeDecodeError:
                raise ValueError(u"Invalid encoding")

        if isinstance(data, unicode) and isinstance(self._schema_validator, Object):
            data = json.loads(data) if len(data) != 0 else {}

        if isinstance(data, (dict, unicode)):
            return data

        raise JSONParserError(u"Unknown json type {}".format(type(data)))

    def _convert(self, data, **kwargs):
        if isinstance(self._schema_validator, Object):
            data = data.copy()
            data.update(kwargs)
            return self._converter(**data)
        else:
            return self._converter(data)

    def parse(self, data, **kwargs):
        if kwargs:
            assert isinstance(self._schema_validator, Object), u"extra named arguments to parse make sense only for " \
                                                               u"Object kind of validators"
        decoded_data = self._decode_data(data)
        try:
            parsed = self._schema_validator.validate(decoded_data)
        except ValidationError as exc:
            errors = {tuple(reversed(exc.context)): exc.msg}
            raise JSONParserError(exc.to_string(), exc.value, errors=errors)

        if self._converter is None:
            return parsed

        if isinstance(self._converter, type):
            try:
                return self._convert(parsed, **kwargs)
            except TypeError as exc:
                message = u"Can't initialize class %s with arguments %s: %s" % (self._converter, data, exc.message)
                raise TypeError(message), None, sys.exc_info()[2]
        else:
            return self._convert(parsed, **kwargs)
