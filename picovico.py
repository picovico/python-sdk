import json
from lib import urls
from lib.session import PicovicoSession
#from lib.api import PicovicoAPIRequest
from lib.helpers import append_music
class Picovico(PicovicoAPIRequest):

	def save(self, auth_session):
		'''
			Picovico: Save the current progress with the project.
		'''
		if not self.video_id:
			return None

		append_music(self.vdd)

		video_assets = {}
		for k,v in self.vdd.items():
			if type(v) is list:
				video_assets[k] = json.dumps(v)
			else:
				video_assets[k] = v

		response = self.post((urls.SAVE_VIDEO).format(self.video_id), data=video_assets, auth_session=auth_session)
		return response

	def preview_video(self, video_id=None, auth_session=None):
		'''
			Picovico:
				Make a preview request for the project. 
				144p video preview is available for the style.
				Rendering state of the video will not be changed.
		'''
		video_response = self.save(auth_session)

		response = self.post((urls.PREVIEW_VIDEO).format(self.get_video_id(video_id)), auth_session=auth_session)
		return response

	def create_video(self, video_id=None, auth_session=None):
		'''
			Picovico: Sends the actual rendering request to rendering engine
		'''
		video_response = self.save(auth_session)
		response = self.post((urls.CREATE_VIDEO).format(self.get_video_id(video_id)), auth_session=auth_session)
		return response

	def duplicate_video(self, video_id, auth_session=None):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
		'''
		response = self.post((urls.DUPLICATE_VIDEO).format(video_id), auth_session=auth_session)
		return response

	def get_video_id(self, video_id):
		return video_id if video_id else self.video_id
		




