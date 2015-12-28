import json
from lib import constants, urls, utils
from lib.api import PicovicoAPIRequest
from lib.components.music import PicovicoMusic
from lib.components.video import PicovicoVideo 
from lib.components.photo import PicovicoPhoto
from lib.components.style import PicovicoStyle
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoProject(PicovicoVideo):

	picovico_session = None

	def __init__(self, picovico_session=None):

		if picovico_session:
			self.auth_headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

		self.pv_photo = PicovicoPhoto(picovico_session)
		self.pv_music = PicovicoMusic(picovico_session)

	def open(self, video_id=None):
		'''
			Picovico: Open any existing project which has not yet been rendered
		'''
		self.video_id = None
		self.vdd = {}
		if video_id:
			picovico_video = self.get_video(video_id)
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
		response = PicovicoAPIRequest.post(url=urls.BEGIN_PROJECT, data=data, headers=self.auth_headers)

		if response['id']:
			self.video_id = response['id']
			self.vdd = response
			self.vdd['assets'] = []

		return self.vdd

	def set_style(self, style_machine_name):
		'''
			Picovico: Defines style for the current video project.
		'''
		if style_machine_name:
			self.vdd['style'] = style_machine_name
			return True
		
		return False

	def add_image(self, image_path, caption="", source="hosted"):
		'''
			Picovico: Add and append image to the current project
		'''
		response = self.pv_photo.upload_image(image_path, source)

		if response['id']:
			self.ProjectHelpers(self).add_library_image(response['id'], self.vdd, caption)

		return response

	def add_text(self, title="", text=""):
		'''
			Picovico: Adds text slide to the project
		'''
		if title or text:
			self.ProjectHelpers(self).append_text_slide(self.vdd, title, text)
			return True
		
		return False

	def add_music(self, music_path):
		'''
			Picovico: Defines the background music
		'''
		response = self.pv_music.upload_music(music_path)

		if response['id']:
			self.ProjectHelpers(self).add_library_music(response['id'], self.vdd)

		return response

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

	def draft(self):
		'''
			Picovico: Returns the current draft saved
		'''
		response = PicovicoAPIRequest.get(urls.GET_DRAFT, headers=self.auth_headers)
		return response

	def dump(self):
		'''
			Picovico: Creates a readable dump of the current project
		'''
		try:
			if self.vdd:
				return self.vdd
		except:
			return False

	def reset(self):
		'''
			Picovico: Resets the current local progress
		'''
		self.ProjectHelpers(self).reset_music(self.vdd)
		self.ProjectHelpers(self).reset_slides(self.vdd)
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

	class ProjectHelpers():

		def __init__(self, project_instance):
			self.project_helpers = project_instance

		def add_library_image(self, image_id, vdd, caption=""):
			'''
			Picovico: Appends any image previously uploaded.
			'''
			if image_id:
				self.append_image_slide(image_id, vdd, caption)
				return True

			return False

		def append_image_slide(self, image_id, vdd, caption=None):
			'''
			Picovico: Appends image slide with given data
			'''
			data = {
				'name': 'image',
				'data':{
					'text': caption,
				},
				'asset_id': image_id
			}
			self.append_vdd_slide(vdd, data)

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
				return vdd

		def append_text_slide(self, vdd, title=None, text=None):
			'''
				Picovico: Prepares the slide data for text slides and appends to the vdd
			'''
			data = {
				'name': 'text',
				'data':{
					'title': title,
					'text': text
				}
			}
			self.append_vdd_slide(vdd, data)

		def add_library_music(self, music_id, vdd):
			'''
				Picovico: Define any previously uploaded music, or any music available from library. 
			'''
			if music_id:
				self.set_music(music_id, vdd)
				return True

			return False

		def set_music(self, music_id, vdd):
			'''
				Picovico:
					Saves music for the current video project.
					Saved separately because only one music is supported.
			'''
			data = {
				'name': 'music',
				'asset_id': music_id,
				'_comment': 'Some cool comment which will replace later'
			}
			vdd['_music'] = data
			self.append_vdd_slide(vdd, vdd['_music'])
			del vdd['_music']

		def save(self, video_id):
			'''
				Picovico: Save the current progress with the project.
			'''
			#self.append_music(self.vdd)

			video_assets = {}
			for k,v in self.project_helpers.vdd.items():
				if type(v) is list:
					video_assets[k] = json.dumps(v)
				else:
					video_assets[k] = v

			response = PicovicoAPIRequest.post((urls.SAVE_VIDEO).format(video_id), data=video_assets, headers=self.project_helpers.auth_headers)
			return response

		def reset_slides(self, vdd):
			'''
				Picovico: Resets slides data i.e assets
			'''
			vdd['assets'] = []

		def reset_music(self, vdd):
			'''
				Picovico: Resets music for the project
			'''
			try:
				if vdd['_music']:
					del vdd['_music']
			except KeyError:
				pass

		# def append_music(self, vdd):
		# 	'''
		# 		Picovico: If music is set and not appended to the VDD slide, appends the music as vdd slide
		# 	'''
		# 	if vdd['_music']:
		# 		self.append_vdd_slide(vdd, vdd['_music'])
		# 		del vdd['_music']

	











	



