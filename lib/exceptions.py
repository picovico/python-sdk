'''
	Picovico: Picovico custom exception classes
'''

class PicovicoUnauthorizedException(Exception):
	'''
		Picovico:
				When the access_key and access_token aren't available
				for the curent session
	'''

	def __init__(self, message=None):
		self.message = "Not Authorised"

	def __str__(self):
		return repr(self.message)

class PicovicoAPIResponseException(Exception):
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
	'''

	def __init__(self, status=None, message=None, data=None):
		self.status = status
		self.message = message
		self.data = data

	def __str__(self):
		return  repr({'error':{'status':self.status,'message': self.message}, 'data': self.data})

class DataNotFound(Exception):
	'''
		Picovico: Exception to be raised if expected data is not found.
	'''
	pass

class VideoIdNotFound(Exception):
	'''
		Picovico: Exception to be raised if video id is not found.
	'''
	pass

class PicovicoSessionRequiredException(Exception):
	'''
		Picovico: Exception to be raised if Picovico session instance is not provided.
	'''
	pass
	