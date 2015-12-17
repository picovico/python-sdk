from lib.session import PicovicoSession
from lib.api import PicovicoAPIRequest
class Picovico(PicovicoSession):

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

		self.picovico_request = PicovicoAPIRequest()

	def open(self, video_id):
		pass

	def begin(self):
		pass

	def preview():
		pass

	def create():
		pass

	def duplicate():
		pass

	def save():
		pass

	def reset():
		pass

	def draft():
		pass

	def single_draft():
		pass

	def dump():
		pass

	def get_styles():
		pass

	def get_musics():
		pass

	def get_library_music():
		pass

	def get_video():
		pass

	def get_videos():
		pass




