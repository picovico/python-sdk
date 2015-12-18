from lib.session import PicovicoSession
from lib.api import PicovicoAPIRequest
class Picovico:
	
	def preview_video(self):
		'''
			Picovico:
				Make a preview request for the project. 
				Will generate 144p video is preview is available for the style.
				Rendering state of the video will not be changed.
		'''
		video_response = self.save()
		response = self.post((urls.PREVIEW_VIDEO).format(self.video_id))
		return response

	def create_video(self):
		'''
			Picovico: Send the actual rendering request to rendering engine
		'''
		video_response = self.save()
		response = self.post((urls.CREATE_VIDEO).format(self.video_id))
		return response

	def duplicate_video(self, video_id):
		'''
			Picovico: Duplicates any video and saves it to the new draft or overwrites if any exists
		'''
		response = self.post((urls.DUPLICATE_VIDEO).format(video_id))
		return response

	def get_draft(video_id=None):
		pass
	




