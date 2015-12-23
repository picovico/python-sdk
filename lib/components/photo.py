from lib.api import PicovicoAPIRequest
from lib.auth.session import PicovicoSession
from lib import utils, urls
from lib.helpers import append_vdd_slide, check_video_data
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoPhoto():
	'''
		Picovico: Library componenet for photo
	'''
	picovico_session = None

	def __init__(self, picovico_session=None):

		if picovico_session:
			self.headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def get_images(self):
		'''
			Picovico: Get authenticated user's photo.
		'''
		response = PicovicoAPIRequest.get(urls.ME_PHOTO, headers=self.headers)

	def upload_image(self, image_path, source=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source)

	# def add_image(self, image_path, caption="", source="hosted"):
	# 	'''
	# 		Picovico: Add and append image to the current project
	# 	'''
	# 	response = self.upload_image(image_path, source, headers=headers)
	# 	if response['id']:
	# 		self.add_library_image(response['id'], vdd, caption)

	# 	return response

	# def add_text(self, title="", text=""):
	# 	'''
	# 		Picovico: Adds text slide to the project
	# 	'''
	# 	if title or text:
	# 		self.append_text_slide(video_data, title, text)
	# 		return True
		
	# 	return False

	def upload_image_file(self, file_path, source=None):
		'''
			Picovico: Checks if the image is uploaded locally and process the requests.
		'''
		if utils.is_local_file(file_path):
			response = PicovicoAPIRequest.put(urls.ME_PHOTO, file_path, headers=self.headers)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = PicovicoAPIRequest.post(urls.ME_PHOTO, data=data, headers=self.headers)
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
		