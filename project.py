from picovico import Picovico
from lib import constants, urls, utils
from lib.api import PicovicoAPIRequest
from lib.components.music import PicovicoMusic
from lib.components.video import PicovicoVideo 
from lib.components.photo import PicovicoPhoto
from lib.components.style import PicovicoStyle
from lib.helpers import reset_slides, reset_music

class PicovicoProject(PicovicoVideo):

	def __init__(self):
		'''
			Picovico: Construction for picovico components object.
		'''
		# self.pv_music = PicovicoMusic()
		# self.pv_photo = PicovicoPhoto()
		# self.pv_style = PicovicoStyle()
		self.pv_request = PicovicoAPIRequest()

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

	# def delete_image(self, image_id, auth_session):
	# 	'''
	# 		Picovico: Deletes uploaded image with given image id.
	# 	'''
	# 	return self.pv_photo.delete_image(image_id, auth_session=auth_session)

	# def upload_image(self, image_path, source=None, auth_session=None):
	# 	'''
	# 		Picovico: Uploads the image to the current project
	# 	'''
	# 	return self.pv_photo.upload_image_file(image_path, source, auth_session=auth_session)

	# def add_image(self, image_path, caption="", source="hosted", auth_session=None):
	# 	'''
	# 		Picovico: Add and append image to the current project
	# 	'''
	# 	response = self.upload_image(image_path, source, auth_session=auth_session)
	# 	if response['id']:
	# 		self.pv_photo.add_library_image(response['id'], self.vdd, caption)

	# 	return response

	# def add_text(self, title="", text=""):
	# 	'''
	# 		Picovico: Adds text slide to the project
	# 	'''
	# 	if title or text:
	# 		self.pv_photo.append_text_slide(self.vdd, title, text)
	# 		return True
		
	# 	return False

	# def upload_music(self, music_path, source=None, auth_session=None):
	# 	'''
	# 		Picovico: Uploads the music file to the current project.
	# 	'''
	# 	return self.pv_music.upload_music_file(music_path, source, auth_session=auth_session)

	# def add_music(self, music_path, auth_session=None):
	# 	'''
	# 		Picovico: Defines the background music
	# 	'''
	# 	response = self.upload_music(music_path, auth_session=auth_session)

	# 	if response['id']:
	# 		self.pv_music.add_library_music(response['id'], self.vdd)

	# 	return response

	# def get_styles(self, auth_session=None):
	# 	'''
	# 		Picovico: Gets available styles
	# 	'''
	# 	return self.pv_style.get_styles(auth_session)

	# def set_style(self, style_machine_name):
	# 	'''
	# 		Picovico: Defines style for the current video project.
	# 	'''
	# 	if style_machine_name:
	# 		self.vdd['style'] = style_machine_name
	# 		return True
		
	# 	return False

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
		response = self.pv_request.get(urls.GET_DRAFT, auth_session=auth_session)
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







	



