import json
from lib import urls
from lib.api import PicovicoAPIRequest
from lib.exceptions import VideoIdNotFound
from lib.messages import VIDEO_ID_NOT_FOUND
from lib.helpers import append_music

class PicovicoVideo(PicovicoAPIRequest):
	'''
		Picovico: Library component for video
	'''
	def get_video(self, video_id, auth_session):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		self.check_video_id(video_id)
		response = self.get((urls.SINGLE_VIDEO).format(video_id), auth_session=auth_session)
		return response

	def get_videos(self, auth_session):
		'''
			Picovico: Get list of 15 videos
		'''
		response = self.get(urls.GET_VIDEOS, auth_session=auth_session)
		return response

	def save(self, video_id, auth_session):
		'''
			Picovico: Save the current progress with the project.
		'''
		self.check_video_id(video_id)
		append_music(self.vdd)

		video_assets = {}
		for k,v in self.vdd.items():
			if type(v) is list:
				video_assets[k] = json.dumps(v)
			else:
				video_assets[k] = v

		response = self.post((urls.SAVE_VIDEO).format(video_id), data=video_assets, auth_session=auth_session)
		return response

	def preview_video(self, video_id, auth_session=None):
		'''
			Picovico:
				Make a preview request for the project. 
				144p video preview is available for the style.
				Rendering state of the video will not be changed.
		'''
		self.check_video_id(video_id)
		video_response = self.save(video_id, auth_session)

		response = self.post((urls.PREVIEW_VIDEO).format(video_id), auth_session=auth_session)
		return response

	def create_video(self, video_id, auth_session=None):
		'''
			Picovico: Sends the actual rendering request to rendering engine
		'''
		self.check_video_id(video_id)
		video_response = self.save(video_id, auth_session)
		response = self.post((urls.CREATE_VIDEO).format(video_id), auth_session=auth_session)
		return response

	def duplicate_video(self, video_id, auth_session=None):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
		'''
		response = self.post((urls.DUPLICATE_VIDEO).format(video_id), auth_session=auth_session)
		return response

	def check_video_id(self, video_id):
		'''
			Picovico: Checks if video id is available for video components
		'''
		if not video_id:
			raise VideoIdNotFound(VIDEO_ID_NOT_FOUND)
		pass