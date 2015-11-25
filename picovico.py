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
		response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.BEGIN_PROJECT, data, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)

		if decoded_response['id']:
			self.video_id = decoded_response['id']
			self.vdd = decoded_response
			self.vdd['assets'] = []

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


	def get_musics(self):
		'''
			Picovico: List all the uploaded musics
		'''
		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.GET_MUSICS, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

	def get_library_musics(self):
		'''
			Picovico: List all the library musics
		'''
		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.GET_LIBRARY_MUSICS, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

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
			response = requests.delete((urls.PICOVICO_API_ENDPOINT + urls.DELETE_MUSIC).format(music_id), headers=self.picovico_auth_headers())
			decoded_response = json.loads(response.text)
			return decoded_response
		
		return False

	def get_styles(self):
		'''
			Picovico: Fetches styles available for the logged in account.
		'''
		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.GET_STYLES, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

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
			self.vdd['credit']
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

	def get(self, video_id):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		response = requests.get((urls.PICOVICO_API_ENDPOINT + urls.SINGLE_VIDEO).format(video_id), headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

	def save(self):
		'''
			Picovico: Save the current progress with the project.
		'''
		if not self.video_id:
			return None


		self.append_music(self.vdd)
		print(self.vdd)
		
		some = {}
		for k,v in self.vdd.items():
			if type(v) is list:
				some[k] = json.dumps(v)
			else:
				some[k] = v

		response = requests.post((urls.PICOVICO_API_ENDPOINT + urls.SAVE_VIDEO).format(self.video_id), data=some, headers=self.picovico_auth_headers())
	
		# decoded_response = json.loads(response.text)
		# return decoded_response
		return (response.text)

	def preview(self):
		'''
			Picovico:
				Make a preview request for the project. 
	 			Will generate 144p video is preview is available for the style.
	 			Rendering state of the video will not be changed.
		'''
		video_response = self.save()
		response = requests.post((urls.PICOVICO_API_ENDPOINT + urls.PREVIEW_VIDEO).format(self.video_id), headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

	def create(self):
		'''
			Picovico: Send the actual rendering request to rendering engine
		'''
		video_response = self.save()
		print("Lets picovico")
		print(video_response)
		print("In the create")
		# print(video_response)
		print(self.vdd)
		response = requests.post((urls.PICOVICO_API_ENDPOINT + urls.CREATE_VIDEO).format(self.video_id), headers=self.picovico_auth_headers())
		print("Hellooww")
		print(response)
		decoded_response = json.loads(response.text)

		return decoded_response

	def duplicate(self, video_id):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overwrites if any exists
		'''
		response = requests.post((urls.PICOVICO_API_ENDPOINT + urls.DUPLICATE_VIDEO).format(video_id), headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

	def get_videos(self):
		'''
			Picovico: Get list of 15 videos
		'''
		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.GET_VIDEOS, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

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
		response = requests.get(urls.PICOVICO_API_ENDPOINT + urls.GET_DRAFT, headers=self.picovico_auth_headers())
		decoded_response = json.loads(response.text)
		return decoded_response

	def dump(self):
		'''
			Picovico: Creates a readable dump of the current project
		'''
		if self.vdd:
			return self.vdd
		return False











