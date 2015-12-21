from lib.api import PicovicoAPIRequest

class PicovicoVideo(PicovicoAPIRequest):
	'''
		Picovico: Library component for video
	'''
	def get_video(self, video_id, auth_session):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		response = self.get((urls.SINGLE_VIDEO).format(video_id), auth_session=auth_session)
		return response
		
	def get_videos(self, auth_session):
		'''
			Picovico: Get list of 15 videos
		'''
		response = self.get(urls.GET_VIDEOS, auth_session=auth_session)
		return response