#from picovico import Picovico
from lib.api import PicovicoAPIRequest
from lib import urls
class PicovicoSession(object):

	def __init__(self):
		'''
			Picovico: Constructor that initialize the app_id and app_secret.
			Also initializes device_id if available, else sets default device_id.
		'''
	def login():
		pass

	def authenticate(self):
		'''
			Picovico: login with app_id and app_secret
		'''
		data={
			'app_id':self.app_id,
			'app_secret':self.app_secret, 
			'device_id':self.device_id
			}

		response = self.picovico_request.post(url=urls.APP_AUTHENTICATE, data=data, is_anonymous=True)
		
		try:
			self.access_key = response['access_key']
			self.access_token = response['access_token']
		except KeyError:
			raise DataNotFound(messages.ACCESS_KEY_AND_ACCESS_TOKEN_MISSING)

		self.set_login_tokens(self.access_key, self.access_token)

		return response

	def set_login_tokens(self, access_key, access_token):
		'''
			Picovico: Set login tokens generated after authentication
		'''
		self.set_tokens(access_key, access_token)

	def set_tokens(self, access_key, access_token):
		'''
			Picovico: Set tokens for validation.
		'''
		self.access_key = access_key
		self.access_token = access_token
	
	def is_logged_in(self, access_key, access_token):
		'''
			Picovico: Check for login using access_key and access_token.
		'''
		try:
			if self.access_key and self.access_token:
				return True
		except:
			return False
		
	def picovico_auth_headers(self):
		'''
			Picovico: Auth headers for request.
		'''
		return {
			"X-Access-Key":self.access_key,
			"X-Access-Token":self.access_token
		}

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = self.picovico_request.get(url=urls.ME, auth_session=None)
		return response

