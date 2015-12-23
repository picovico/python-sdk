#from picovico import Picovico
from lib import constants, urls, utils
from lib.api import PicovicoAPIRequest
from lib.components.music import PicovicoMusic
from lib.components.video import PicovicoVideo 
from lib.components.photo import PicovicoPhoto
from lib.components.style import PicovicoStyle
from lib.helpers import reset_slides, reset_music
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE

class PicovicoProject(PicovicoVideo):

	picovico_session = None

	def __init__(self, picovico_session=None):
		
		if picovico_session:
			self.headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)


	def open(self, video_id=None):
		'''
			Picovico: Open any existing project which has not yet been rendered
		'''
		self.video_id = None
		self.vdd = {}
		if video_id:
			picovico_video = self.get(video_id)
			if picovico_video['status'] == constants.VIDEO_INITIAL:
				self.video_id = video_id
				self.vdd = picovico_video

				quality_cleanups = []
				for some_quality in self.vdd['quality']:
					quality_cleanups.append(some_quality)

				self.vdd['quality'] = max(quality_cleanups)

			else:
				return False

		return self.vdd

	def begin(self, name, quality=constants.Q_360P):
		'''
			Picovico: Begin the project
		'''
		self.video_id = None
		self.vdd = {}
		data = {
			'name': name,
			'quality': quality,
		}
		response = self.post(url=urls.BEGIN_PROJECT, data=data, headers=self.headers)

		if response['id']:
			self.video_id = response['id']
			self.vdd = response
			self.vdd['assets'] = []

		return self.vdd

	def add_credits(self, title=None, text=None):
		'''
			Picovico: Append credit slide to the current project
		'''
		if title or text:
			if not self.vdd['credit']:
				self.vdd['credit'] = []

			credit_list = [title, text] 
			self.vdd['credit'].append(credit_list)
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

	def draft(self, auth_session=None):
		'''
			Picovico: Returns the current draft saved
		'''
		response = PicovicoAPIRequest.get(urls.GET_DRAFT, headers=self.headers)
		return response

	def dump(self):
		'''
			Picovico: Creates a readable dump of the current project
		'''
		if self.vdd:
			return self.vdd
		return False

	def reset(self):
		'''
			Picovico: Resets the current local progress
		'''
		reset_music(self.vdd)
		reset_slides(self.vdd)
		self.remove_credits()
		self.vdd['style'] = None
		self.vdd['quality'] = None
		return self.vdd

	def set_quality(self, quality):
		'''
			Picovico: Defines rendering quality for the current video project
		'''
		if quality:
			self.vdd['quality'] = quality
			return True
			
		return False







	



