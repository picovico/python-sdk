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

	def upload_image(self, image_path, source=None, auth_session=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source, auth_session=auth_session)

	def upload_image_file(self, file_path, source=None, auth_session=None):
		'''
			Picovico: Checks if the image is uploaded locally and process the requests.
		'''
		if utils.is_local_file(file_path):
			response = self.put(urls.UPLOAD_PHOTO, file_path, auth_session=auth_session)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = self.post(urls.UPLOAD_PHOTO, data=data, auth_session=auth_session)
			return response

	def upload_music(self, music_path, source=None, auth_session=None):
		'''
			Picovico: Uploads the music file to the current project.
		'''
		return self.upload_music_file(music_path, source, auth_session=auth_session)

	def upload_music_file(self, file_path, source=None):
		'''
			Picovico: Checks if the music is uploaded locally and proecess the requests.
		'''
		if utils.is_local_file(file_path):
			data = {
				'X-Music-Artist': "Unknown",
				"X-Music-Title": "Unknown - {}".format('r')
			}
			response = self.put(urls.UPLOAD_MUSIC, file_path, data)
			return response
		else:
			data = {
				'url': file_path,
				'preview_url': file_path
			}
			response = self.post(urls.UPLOAD_MUSIC, data)
			return response

	def add_image():
		pass

	def add_library_image():
		pass

	def add_text():
		pass

	def add_music():
		pass

	def add_library_music():
		pass

	def delete_music():
		pass

	def delete_music():
		pass

	def set_styles():
		pass

	def set_quality():
		pass

	def set_credits():
		pass

	def remove_credits():
		pass

	def set_callback_url():
		pass

	def save():
		pass

	def reset():
		pass

	def dump():
		pass



	def append_image_slide(self, vdd, image_id, caption=None):

		data = {
			'name': 'image',
			'data':{
				'text': caption,
			},
			'asset_id': image_id
		}
		self.append_vdd_slide(vdd, data)

	def append_vdd_slide(self, vdd, slide):

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
			slide['end_time'] = last_end_time + self.STANDARD_SLIDE_DURATION

			vdd['assets'].append(slide)

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

	def set_music(self, vdd, music_id):
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

	def append_music(self, vdd):
		'''
			Picovico: If music is set and not appended to the VDD slide, appends the music as vdd slide
		'''
		if vdd['_music']:
			self.append_vdd_slide(vdd, vdd['_music'])
			del vdd['_music']

	def reset_slides(self, vdd):
		vdd['assets'] = []

	def reset_music(self, vdd):
		del vdd['_music']







