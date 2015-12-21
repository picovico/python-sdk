from lib.api import PicovicoAPIRequest
from lib import utils, urls
from lib.helpers import append_vdd_slide, check_video_data

class PicovicoPhoto(PicovicoAPIRequest):
	'''
		Picovico: Library componenet for photo
	'''
	def get_images(self, auth_session):
		'''
			Picovico: Get authenticated user's photo.
		'''
		response = self.get(urls.ME_PHOTO, auth_session=auth_session)

	def upload_image(self, image_path, source=None, auth_session=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source, auth_session=auth_session)

	def add_image(self, image_path, caption="", source="hosted", video_data=None, auth_session=None):
		'''
			Picovico: Add and append image to the current project
		'''
		check_video_data(video_data)
		response = self.upload_image(image_path, source, auth_session=auth_session)
		if response['id']:
			self.add_library_image(response['id'], video_data, caption)

		return response

	def add_text(self, title="", text="", video_data=None):
		'''
			Picovico: Adds text slide to the project
		'''
		check_video_data(video_data)
		if title or text:
			self.append_text_slide(video_data, title, text)
			return True
		
		return False

	def upload_image_file(self, file_path, source=None, auth_session=None):
		'''
			Picovico: Checks if the image is uploaded locally and process the requests.
		'''
		if utils.is_local_file(file_path):
			response = self.put(urls.ME_PHOTO, file_path, auth_session=auth_session)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = self.post(urls.ME_PHOTO, data=data, auth_session=auth_session)
			return response

	def delete_image(self, image_id, auth_session):
		'''
			Picovico: Deletes uploaded image
		'''
		return self.delete((urls.ME_PHOTO_DELETE).format(image_id), auth_session=auth_session)

	'''
		Picovico: Helpers for image component processing
	'''

	def add_library_image(self, image_id, vdd, caption=""):
		'''
			Picovico: Appends any image previously uploaded.
		'''
		if image_id:
			self.append_image_slide(vdd, image_id, caption)
			return True

		return False

	def append_image_slide(self, vdd, image_id, caption=None):
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
		append_vdd_slide(vdd, data)

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
		append_vdd_slide(vdd, data)
		