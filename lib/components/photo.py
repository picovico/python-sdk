from lib.api import PicovicoAPIRequest
from lib import utils, urls
from lib.helpers import append_vdd_slide

class PicovicoPhoto(PicovicoAPIRequest):
	'''
		Picovico: Library componenet for photo
	'''
	def get_images(self, auth_session):
		'''
			Picovico: Get authenticated user's photo.
		'''
		response = self.get(urls.ME_PHOTO, auth_session=auth_session)

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
		