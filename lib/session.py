#from picovico import Picovico
from lib.api import PicovicoAPIRequest #as picovico_request
from lib import urls
class PicovicoSession(PicovicoAPIRequest):

	# access_key = None
	# access_token = None
	# app_id = None
	# app_secret = None
	# device_id = None

	def __init__(self, app_id=None, app_secret=None, device_id=None):#, access_key=None, access_token=None):
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

		response = self.post(url=urls.APP_AUTHENTICATE, data=data, is_anonymous=True)

		if not response.get('access_key') and response.get('access_token'):
			raise DataNotFound(messages.ACCESS_KEY_AND_ACCESS_TOKEN_MISSING)

		return response
		
	def profile(self, auth_session=None):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = self.get(url=urls.ME, auth_session=auth_session)
		return response

