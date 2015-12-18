from picovico.lib.api import PicovicoApiRequest

class PicovicoVideo(PicovicoApiRequest):
	'''
		Picovico: Library component for video
	'''
	def get_video(self, video_id):
		'''
			Picovico: Fetch any existing video. Use open() for editing.
		'''
		response = self.get((urls.SINGLE_VIDEO).format(video_id))
		return response
	def get_videos():
		pass

	def set_quality(self, quality):
		'''
			Picovico: Defines rendering quality for the current video project
		'''
		if quality:
			self.vdd['quality'] = quality
			return True
			
		return False