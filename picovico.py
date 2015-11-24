import requests, json, sys
from lib import config, urls
from lib.base import PicovicoBase
from lib.constants import PicovicoConstants


class Picovico(PicovicoBase, PicovicoConstants):

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

	def authenticate(self):
		'''
			Picovico: login with app_id and app_secret
		'''
		data={
			'app_id':self.app_id,
			'app_secret':self.app_secret, 
			'device_id':self.device_id
			}

		response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.APP_AUTHENTICATE, data)
		decoded_response = json.loads(response.text)

		try:
			self.access_key = decoded_response['access_key']
			self.access_token = decoded_response['access_token']
		except KeyError:
			pass

		if self.access_key and self.access_token:
			self.set_login_tokens(self.access_key, self.access_token)

		return (decoded_response)

	def set_login_tokens(self, access_key, access_tokens):
		'''
			Picovico: Set login tokens generated after authentication
		'''
		self.set_tokens(access_key, access_tokens)

	def profile(self):
		'''
			Picovico: generate profile for authenticated user
		'''

		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.ME, headers=self.picovico_auth_headers())
		return (json.loads(response.text))


	def open(self, video_id):
		pass

	def begin(self, name, quality=360): 
		'''
			Picovico: Begin the project
		'''
		self.video_id = None
		self.vdd = {}
		data = {
			'name': name,
			'quality': quality,
		}
		response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.BEGIN_PROJECT, data, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)

		if decoded_response['id']:
			self.video_id = decoded_response['id']
			self.vdd = decoded_response
			self.vdd['assets'] = {}

		return self.video_id

	def upload_image(self, image_path, source=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source)

	def upload_music(self, music_path, source=None):
		'''
			Picovico: Uploads the music file to the current project.
		'''
		return self.upload_music_file(music_path, source)

	def add_image(self, image_path, caption="", source="hosted"):
		'''
			Picovico: Add and append image to the current project
		'''
		response = self.upload_image(image_path, source)
		
		if response['id']:
			self.add_library_image(response['id'], caption)

		return response


	def add_library_image(self, image_id, caption=""):
		'''
			Picovico: Appends any image previously uploaded.
		'''
		if image_id:
			self.append_image_slide(self.vdd, image_id, caption)
			return True
		return False





