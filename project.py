from picovico import Picovico
from lib import constants, urls, utils
from lib.api import PicovicoAPIRequest
class PicovicoProject(Picovico, PicovicoAPIRequest):

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

	def begin(self, name, quality=constants.Q_360P, auth_session=None): 
		'''
			Picovico: Begin the project
		'''
		self.video_id = None
		self.vdd = {}
		data = {
			'name': name,
			'quality': quality,
		}
		response = self.post(url=urls.BEGIN_PROJECT, data=data, auth_session=auth_session)

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



	def append_vdd_slide(self, vdd, slide):
		'''
			Picovico: Appends image slides into the project with data
		'''
		if vdd:
			if not vdd['assets']:
				vdd['assets'] = []

			last_slide = None
			current_slides_count = len(vdd['assets'])
			last_end_time = 0

			if vdd['assets']:
				last_slide = vdd['assets'][len(vdd['assets']) - 1]

				if last_slide:
					last_end_time = last_slide["end_time"]
				else:
					last_end_time = last_slide.end_time

			slide['start_time'] = last_end_time
			slide['end_time'] = last_end_time + constants.STANDARD_SLIDE_DURATION

			vdd['assets'].append(slide)


	def draft(self):
		'''
			Picovico: Returns the current draft saved
		'''
		response = self.get(urls.GET_DRAFT)
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
		self.reset_music(self.vdd)
		self.reset_slides(self.vdd)
		self.remove_credits()
		self.vdd['style'] = None
		self.vdd['quality'] = None
		return self.vdd





	



