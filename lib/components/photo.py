from lib.api import PicovicoAPIRequest
from lib.auth.session import PicovicoSession
from lib import utils, urls
from lib.helpers import append_vdd_slide, check_video_data

class PicovicoPhoto(PicovicoSession):
	'''
		Picovico: Library componenet for photo
	'''
	def get_images(self, headers):
		'''
			Picovico: Get authenticated user's photo.
		'''
		response = PicovicoAPIRequest.get(urls.ME_PHOTO, headers=headers)

	def upload_image(self, image_path, source=None, headers=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source, headers=headers)

	def add_image(self, image_path, caption="", source="hosted", video_data=None, headers=None):
		'''
			Picovico: Add and append image to the current project
		'''
		check_video_data(video_data)
		response = self.upload_image(image_path, source, headers=headers)
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

	def upload_image_file(self, file_path, source=None, headers=None):
		'''
			Picovico: Checks if the image is uploaded locally and process the requests.
		'''
		if utils.is_local_file(file_path):
			response = PicovicoAPIRequest.put(urls.ME_PHOTO, file_path, headers=headers)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = PicovicoAPIRequest.post(urls.ME_PHOTO, data=data, headers=headers)
			return response

	def delete_image(self, image_id, headers=None):
		'''
			Picovico: Deletes uploaded image
		'''
		return PicovicoAPIRequest.delete((urls.ME_PHOTO_DELETE).format(image_id), headers=headers)

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
		