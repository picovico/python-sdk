"""
	Picovico: Picovico custom exception classes
"""
"""
Picovico:
	When the access_key and access_token aren't available
	for the curent session
"""
class PicovicoUnauthorizedException(Exception):

	def __init__(self, message=None):
		self.message = "Not Authorised"

	def __str__(self):
		return repr(self.message)

"""
Picovico:
	When the response status code is not 200
	Something like : 
	{
		"error":{
			'status': 400,
			'message': "Some messages"
		}
	}
"""
class PicovicoAPIResponseException(Exception):

	def __init__(self, status=None, message=None, data=None):
		self.status = status
		self.message = message
		self.data = data

	def __str__(self):
		return  repr({'error':{'status':self.status,'message': self.message}, 'data': self.data})

class DataNotFound(Exception):
	pass

class VideoIdNotFound(Exception):
	pass

class PicovicoSessionRequiredException(Exception):
	pass
	