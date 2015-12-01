import requests, json, sys
from lib import config, urls, messages
from lib.base import PicovicoBase
from lib.api import PicovicoAPIRequest
from lib.constants import PicovicoConstants
from lib.uploads import PicovicoUploads
from lib.exceptions import PicovicoAPIResponseException, PicovicoUnauthorizedException, DataNotFound

class Picovico(PicovicoConstants, PicovicoUploads):

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

	def login(self, username, password, app_id):
		'''
			Picovico: Login with username and password. APP_ID is mendetory for both logins
		'''
		if username and password:
			data = {
				'username': username,
				'password': password,
				'app_id' : app_id,
				'device_id': self.device_id
			}

			response = self.post(urls.LOGIN, data=data)
			try:
				self.access_key = response['access_key']
				self.access_token = response['access_token']
			except KeyError:
				raise DataNotFound("Not authorised")

			self.set_login_tokens(self.access_key, self.access_token)

			return response

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
		
		try:
			self.access_key = response['access_key']
			self.access_token = response['access_token']
		except KeyError:
			raise DataNotFound(messages.ACCESS_KEY_AND_ACCESS_TOKEN_MISSING)

		self.set_login_tokens(self.access_key, self.access_token)

		return response

	def set_login_tokens(self, access_key, access_tokens):
		'''
			Picovico: Set login tokens generated after authentication
		'''
		self.set_tokens(access_key, access_tokens)

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = self.get(url=urls.ME)
		return response

	def open(self, video_id=None):
		'''
			Picovico: Open any existing project which has not yet been rendered
		'''
		self.video_id = None
		self.vdd = {}
		if video_id:
			picovico_video = self.get(video_id)
			if picovico_video['status'] == self.VIDEO_INITIAL:
				self.video_id = video_id
				self.vdd = picovico_video

				quality_cleanups = []
				for some_quality in self.vdd['quality']:
					quality_cleanups.append(some_quality)

				self.vdd['quality'] = max(quality_cleanups)

			else:
				return False

		return self.vdd

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
		response = self.post(url=urls.BEGIN_PROJECT, data=data)

		if response['id']:
			self.video_id = response['id']
			self.vdd = response
			self.vdd['assets'] = []

		return self.vdd

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

	def get_musics(self):
		'''
			Picovico: List all the uploaded musics
		'''
		response = self.get(urls.GET_MUSICS)
		return response

	def get_library_musics(self):
		'''
			Picovico: List all the library musics
		'''
		response = self.get(urls.GET_LIBRARY_MUSICS)
		return response
		
	def add_text(self, title="", text=""):
		'''
			Picovico: Adds text slide to the project
		'''
		if title or text:
			self.append_text_slide(self.vdd, title, text)
			return True
		
		return False

	def add_music(self, music_path):
		'''
			Picovico: Defines the background music
		'''
		response = self.upload_music(music_path)

		if response['id']:
			self.add_library_music(response['id'])

		return response

	def add_library_music(self, music_id):
		'''
			Picovico: Define any previously uploaded music, or any music available from library. 
		'''
		if music_id:
			self.set_music(self.vdd, music_id)
			return False

		return True

	def delete_music(self, music_id):
		'''
			Picovico: Deletes the music from your library
		'''
		if music_id:
			response = self.delete((urls.DELETE_MUSIC).format(music_id))
			return response
		return False

	def get_styles(self):
		'''
			Picovico: Fetches styles available for the logged in account.
		'''
		response = self.get(urls.GET_STYLES)
		return response

	def set_style(self, style_machine_name):
		'''
			Picovico: Defines style for the current video project.
		'''
		if style_machine_name:
			self.vdd['style'] = style_machine_name
			return True
		
		return False

	def set_quality(self, quality):
		'''
			Picovico: Defines rendering quality for the current video project
		'''
		if quality:
			self.vdd['quality'] = quality
			return True

		return False

	def add_credits(self, title=None, text=None):
		'''
			Picovico: Append credit slide to the current project
		'''
		if title or text:

			if not self.vdd['credit']:
				self.vdd['credit'] = []

			credit_list = [title, text] 

			self.vdd['credit'].append(credit_list)
			# self.vdd['credit']
			return True

		return False

	def remove_credits(self):
		'''
			Picovico: Removes all credit slides
		'''
		if self.vdd['credit']:
			self.vdd['credit'] = []
			return True

		return False

	def set_callback_url(self, url):
		'''
			Picovico: Sets callback url.
		'''
		self.vdd['callback_url'] = url
		return True

	def get_video(self, video_id):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		response = self.get((urls.SINGLE_VIDEO).format(video_id))
		return response

	def save(self):
		'''
			Picovico: Save the current progress with the project.
		'''
		if not self.video_id:
			return None

		self.append_music(self.vdd)

		video_assets = {}
		for k,v in self.vdd.items():
			if type(v) is list:
				video_assets[k] = json.dumps(v)
			else:
				video_assets[k] = v

		response = self.post((urls.SAVE_VIDEO).format(self.video_id), data=video_assets)
		return response

	def preview(self):
		'''
			Picovico:
				Make a preview request for the project. 
				Will generate 144p video is preview is available for the style.
				Rendering state of the video will not be changed.
		'''
		video_response = self.save()
		response = self.post((urls.PREVIEW_VIDEO).format(self.video_id))
		return response

	def create(self):
		'''
			Picovico: Send the actual rendering request to rendering engine
		'''
		video_response = self.save()
		response = self.post((urls.CREATE_VIDEO).format(self.video_id))
		return response

	def duplicate(self, video_id):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overwrites if any exists
		'''
		response = self.post((urls.DUPLICATE_VIDEO).format(video_id))
		return response

	def get_videos(self):
		'''
			Picovico: Get list of 15 videos
		'''
		response = self.get(urls.GET_VIDEOS)
		return response

	def reset(self):
		'''
			Picovico: Resets the current local progress
		'''
		self.reset_music(self.vdd)
		self.reset_slides(self.vdd)
		self.remove_credits()
		self.vdd['style'] = None
		self.vdd['quality'] = None
		return self.vdd

	def draft(self):
		'''
			Picovico: Returns the current draft saved
		'''
		response = self.get(urls.GET_DRAFT)
		return response

	def single_draft(self, draft_id):
		'''
			Picovico: Returns single draft by id
		'''
		response = self.get((urls.GET_SINGLE_DRAFT).format(draft_id))
		return response

	def dump(self):
		'''
			Picovico: Creates a readable dump of the current project
		'''
		if self.vdd:
			return self.vdd
		return False







