import json
from lib import urls
from lib.api import PicovicoAPIRequest
from lib.exceptions import VideoIdNotFound, PicovicoSessionRequiredException
from lib.messages import VIDEO_ID_NOT_FOUND, SESSION_REQUIRED_MESSAGE


class PicovicoVideo(PicovicoAPIRequest):
	'''
		Picovico: Library component for video
	'''
	picovico_session = None

	def __init__(self, picovico_session=None):

		if picovico_session:
			self.headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def get_video(self, video_id):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		response = self.get((urls.SINGLE_VIDEO).format(video_id), headers=self.headers)
		return response

	def get_videos(self):
		'''
			Picovico: Get list of 15 videos
		'''
		response = self.get(urls.GET_VIDEOS, headers=self.headers)
		return response

	def preview_video(self, video_id):
		'''
			Picovico:
				Make a preview request for the project. 
				144p video preview is available for the style.
				Rendering state of the video will not be changed.
		'''
		if video_id is None:
			raise VideoIdNotFound(VIDEO_ID_NOT_FOUND)

		video_response = self.save(video_id)

		response = self.post((urls.PREVIEW_VIDEO).format(video_id), headers=self.headers)
		return response

	def create_video(self, video_id):
		'''
			Picovico: Sends the actual rendering request to rendering engine
		'''
		if video_id is None:
			raise VideoIdNotFound(VIDEO_ID_NOT_FOUND)

		video_response = self.save(video_id)
		response = self.post((urls.CREATE_VIDEO).format(video_id), headers=self.headers)
		return response

	def duplicate_video(self, video_id):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
		'''
		response = self.post((urls.DUPLICATE_VIDEO).format(video_id), headers=self.headers)
		return response
