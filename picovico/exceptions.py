'''	Picovico-SDK: Custom exception classes
    ======================================
'''
class PicovicoError(Exception):
    """ Picovico-SDK: Base Class for all request errors.

    This is the base class for mostly API call errors.

    Args:
        status(int): HTTP status code.
        message(str): Readable message.
        response(:class:`dict` | :mod:`json`): Raw response from request itself.
    """

    def __init__(self, status=None, message=None, response=None):
        self.status = status
        self.message = message
        self.raw_response = response

    def __str__(self):
        return  repr({'error':{'status':self.status,'message': self.message}, 'response': self.raw_response})


class PicovicoRequestError(PicovicoError):
    """ Picovico-SDK: Class for all the client related request errors.

    This class is raised when the response from server is not related to
    200 or 300 and 500 status.
	"""

    def __init__(self, status=400, message=None, response=None):
        assert 400 <= status <=499, 'Only greater than 400 HTTP status allowed.'
        super(PicovicoRequestError, self).__init__(status, message, response)


class PicovicoNotFound(PicovicoRequestError):
    """ Picovico-SDK:  Error for 404 status."""

    def __init__(self, message=None, response=None):
        super(PicovicoNotFound, self).__init__(status=404, message=message, response=response)


class PicovicoUnauthorized(PicovicoNotFound):
    """ Picovico-SDK: Error for 401 status.

    This error is raised when there is fault in access-token
    and access-key scenario. i.e. Authentication problems.
	"""

    def __init__(self, message=None, response=None):
        super(PicovicoNotFound, self).__init__(status=401, message=message, response=response)



class PicovicoServerError(PicovicoError):
    """ Picovico-SDK: Same as :class:`.PicovicoRequestError`.

    This is raised for status codes of 500 i.e. server related errors.
    """

    def __init__(self, status=500, message=None, response=None):
        assert 500 <= status <= 505, 'Only greater than 500 HTTP status allowed'
        super(PicovicoServerError, self).__init__(status, message, response)


class PicovicoAPINotAllowed(Exception):
    """ Picovico-SDK: Helper class for  API errors.

    This class is raised when there is some api related thresholds.
    """
    pass


class PicovicoComponentNotSupported(Exception):
    """ Picovico-SDK: Helper class for component errors.

    This is raised when user sets component that is not yet supported.
    """
    pass


class PicovicoProjectNotAllowed(Exception):
    """ Picovico-SDK: Project related error class.

    This is raised when there is some assertions in project
    methods.
    """
    pass

def raise_valid_error(**error_response):
    """ Picovico-SDK: Exception raising helper.
    Raises valid errors according to status_code provided.

    Args:
        status_code(int): HTTP status code either from response itself or provided explicitly.

    Raises:
        PicovicoNotFound
        PicovicoUnauthorized
        PicovicoRequestError
        PicovicoServerError
    """
    status = error_response.pop('status_code')
    exc_args = {
        'response': error_response.copy()
    }
    if 'error' in error_response:
        error_response = error_response['error']
    exception_map = {
        404: PicovicoNotFound,
        401: PicovicoUnauthorized,
    }
    if status not in exception_map:
        exc_args.update(status=status)
    exc_args.update(message=error_response.get('message', "There was a error."))
    if status >= 500:
        ExceptionClass = PicovicoServerError
    else:
        ExceptionClass = exception_map.get(status, PicovicoRequestError)
    raise ExceptionClass(**exc_args)
