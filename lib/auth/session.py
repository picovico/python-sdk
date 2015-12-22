from lib.api import PicovicoAPIRequest
from lib import urls, exceptions


class PicovicoSession:

	access_key = None
	access_token = None
	app_id = None
	app_secret = None
	device_id = None

	def __init__(self, app_id=None, app_secret=None, device_id=None):
		'''
			Picovico: Constructor that initialize the app_id and app_secret.
			Also initializes device_id if available, else sets default device_id.
		'''
		self.app_id = app_id
		self.app_secret = app_secret

		if not device_id:
			self.device_id = "com.picovico.api.python-sdk"
		else:
			self.device_id = device_id

	def set_auth_tokens(self, access_key, access_token, user_id=None):
		self.access_key = access_key
		self.access_token = access_token

	def _get_auth_headers(self, is_anonymous=False):
		'''
		Picovico: Checks if user is anonymous and returns exceptis if it is.
		'''
		if is_anonymous:
			return {
				"X-Access-Key":None,
				"X-Access-Token":None
			}
		if not is_anonymous and not self.is_logged_in():
			raise exceptions.PicovicoUnauthorizedException()

		return {
			"X-Access-Key":self.access_key,
			"X-Access-Token":self.access_token
		}

	def is_logged_in(self):
		'''
			Picovico: Checks if user is logged in with access_key and access_token
		'''
		return self.access_token and self.access_key


	def login(self, username, password, app_id):
		'''
			Picovico: Login with username and password. APP_ID is mendetory for both logins
		'''
		if username and password:
			data = {
				'username': username,
				'password': password,
				'app_id' : self.app_id,
				'device_id': self.device_id
			}

			response = PicovicoAPIRequest.post(urls.LOGIN, data=data)

			if not response.get('access_key') and response.get('access_token'):
				raise DataNotFound(messages.ACCESS_KEY_AND_ACCESS_TOKEN_MISSING)

			self.set_auth_tokens(access_key=response.get('access_key'), 
				access_token=response.get('access_token'), 
				user_id=response.get('id'))
			
			return True

	def authenticate(self):
		'''
			Picovico: login with app_id and app_secret
		'''
		data={
			'app_id':self.app_id,
			'app_secret':self.app_secret, 
			'device_id':self.device_id
			}

		response = PicovicoAPIRequest.post(url=urls.APP_AUTHENTICATE, data=data)

		if not response.get('access_key') and response.get('access_token'):
			raise DataNotFound(messages.ACCESS_KEY_AND_ACCESS_TOKEN_MISSING)

		self.set_auth_tokens(access_key=response.get('access_key'), 
			access_token=response.get('access_token'), 
			user_id=response.get('id'))

		return True

	def logout(self):
		'''
			Picovico: 
		'''
		self.access_key = None
		self.access_token = None
		self.user_id = None


