from abc import abstractmethod, ABCMeta


class BaseRequestContext(object):
    def __init__(self, user_id, request_uri):
        self.user_id = user_id
        self.request_uri = request_uri

class ApiHandlerMeta(object):
    __metaclass__ = ABCMeta

    def __init__(self, context):
        """

        :param context:
        :return:
        """
        self.context = context

    # @staticmethod
    # def success(result):
    #     return SuccessApiResponse(result)
    #
    # @staticmethod
    # def created(result):
    #     return CreatedApiResponse(result)
    #
    # @staticmethod
    # def updated(result):
    #     return UpdatedApiResponse(result)
    #
    # @staticmethod
    # def deleted(result):
    #     return DeletedApiResponse(result)
    #
    # @staticmethod
    # def unexpected_error(reason):
    #     return UnexpectedApiError(reason)
    #
    # @staticmethod
    # def cont(destination, content_type="text/plain"):
    #     return ContinueApiResponse(destination, content_type)
    #
    # @staticmethod
    # def validation_error(argument, problem):
    #     return ValidationApiError([ValidationProblem(argument, problem)])
    #
    # @staticmethod
    # def multi_validation_error(problems):
    #     return ValidationApiError(problems)
    #
    # @staticmethod
    # def forbidden_error(message):
    #     return ForbiddenApiError(message)
    #
    # @staticmethod
    # def not_acceptable_error(reason):
    #     return NotAcceptableApiError(reason)
    #
    # @staticmethod
    # def not_found_error(object_type, object_id):
    #     return NotFoundApiError(object_type, object_id)
    #
    # @staticmethod
    # def payment_required_error(payment_type):
    #     return PaymentRequiredApiError(payment_type)
    #
    # @staticmethod
    # def handler_not_found_error():
    #     return HandlerNotFoundApiError()

    def validate_arguments(self, arguments, payload):
        """
        Validation step that's happening in `validate_arguments` function should check request provided by technology
        abstraction layer versus basic rules for validity. Any errors found must cause ValidationApiError exception
        raised. None value returned from this function indicates that no errors in request were found.

        This processing MUST NOT involve any DB-related operations and MUST be performed in functionally-clean way, e.g.
        same input must give same output under any conditions.

        Examples of tasks that should be performed there:
          * parse JSON and check it's structure versus schema
          * check correctness of enumerated values in arguments, like sort type and direction
          * TBD

        Error handling
        ----------------

        Normally validation of request SHOULD NOT throw any exceptions. Any expected exceptions MUST be handled by the
        function itself. Any unexpected exceptions MUST be propagated to caller (that means no `except Exception:`
        section)

        :param arguments: dictionary of argument names as keys and their unicode values
        :type arguments: dict
        :param payload: array of bytes representing any payload part of request
        :type payload: str
        :return: None
        :rtype: NoneType
        :raises: ValidationApiError
        """
        pass

    @abstractmethod
    def decode(self, arguments, payload):
        """
        Decoding step that's happening in `decode` function should transform request provided by technology abstraction
        layer into domain-specific request object. Decoding step can throw validation errors because sometimes domain
        domain-specific request can't be constructed with data provided.

        Examples of tasks that should be performed there:
          * parse JSON into Python structure
          * extract data from parsed arguments
          * split compound arguments like sort=name:ascending
          * handle possible errors (see below)

        Error handling
        ----------------

        If there're not enough arguments to construct request object or argument values are invalid then decode function
        must raise DecodeError exception with message describing the problem happened.

        Any known exception thrown during construction of request object must be catch up and transformed to
        ValidationApiError with relevant error message. Unexpected exceptions MUST NOT be catched (e.g. no
        `catch Exception:` sections).

        :param arguments: dictionary of argument names as keys and their unicode values
        :type arguments: dict
        :param payload: array of bytes representing any payload part of request
        :type payload: str
        :return domain-specific request object, accepted by other functions in ApiHandler implementation
        :rtype: DomainSpecificRequest
        :raises: ValidationApiError
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, request):
        """
        Processing step that's happening in `handle` function has the goal of performing actual workload associated
        with request. This function assumes that passed request object is correct and SHOULD NOT apply any additional
        validations to it. This is the step where actual calls to DB models, resources and controllers can be made.

        Error handling
        ----------------

        We can't expect that request handling will always go well and must be ready for different kinds of exceptions.
        This function must catch all expected exceptions that can happen during request processing and transform them
        into one of error classes provided by framework (TBD).
        - ValidationApiError

        `handle` function MUST NOT try to catch unknown errors (no `catch Exception:` section).

        :param request: validated domain-specific request object
        :type request: DomainSpecificRequest
        :return: request-specific processing result
        :rtype: object
        """
        raise NotImplementedError

    @abstractmethod
    def encode(self, request, result):
        """
        Encoding step that's happening in `encode` must transform result of request processing obtained from `handle`
        function to the format that is accepted by API caller. Format details can be possibly specified in request, so
        this function accepts both request and result objects as its arguments.

        Return value of this function must be array of bytes (`str` object) with result encoded into required format.

        Error handling
        ---------------

        Normally encoding of results MUST NOT throw any exceptions. Any expected exceptions MUST be handled by the
        function itself. Any unexpected exceptions MUST be propagated to caller (that means no `except Exception:`
        section)

        :param request: validated domain specific request object
        :type request: DomainSpecificRequest
        :param result: request-specific processing result
        :rtype: object
        :return: encoded result
        :rtype: str
        """
        raise NotImplementedError