'''
	Picovico: Picovico custom exception classes
'''
import six


class PicovicoRequestError(Exception):
	'''
		Picovico:
				When the api response status code is not 200
				Error should be something like :
								{
								"error":{
										'status': 400,
										'message': "Some messages"
									}
							}
        Args:
            status(int): HTTP status code.
            message(str): Readable message.
            response(dict, json): Raw response.
	'''

	def __init__(self, status=None, message=None, response=None):
		self.status = status
		self.message = message
		self.raw_response = response

	def __str__(self):
		return  repr({'error':{'status':self.status,'message': self.message}, 'response': self.raw_response})

class PicovicoNotFound(PicovicoRequestError):

    def __init__(self, message=None, response=None):
        super(PicovicoNotFound, self).__init__(status=404, message=message, response=response)


class PicovicoUnauthorized(PicovicoNotFound):
    '''
		Picovico: When the access_key and access_token aren't available
				for the curent session
	'''
    def __init__(self, message=None, response=None):
        super(PicovicoNotFound, self).__init__(status=401, message=message, response=response)

class PicovicoServerError(PicovicoRequestError):
    pass

class PicovicoAPINotAllowed(Exception):
    pass

class PicovicoComponentNotSupported(Exception):
    pass

#utility to filter exceptions
def raise_valid_exceptions(**error_response):
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
