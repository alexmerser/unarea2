class DocumentValidationError(StandardError):
    pass

class InvalidKeyValueError(Exception):
    pass


class UnexpectedKeyError(Exception):
    pass


class DuplicateKeyError(Exception):
    pass