from lib import utils, urls
from lib.api import PicovicoAPIRequest
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoPhoto():
	'''
		Picovico: Library componenet for photo
	'''
	picovico_session = None

	def __init__(self, picovico_session=None):
		'''
			Picovico: Constructor to accept session instance. If not, will raise exception.
		'''
		if picovico_session:
			self.auth_headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def get_images(self):
		'''
			Picovico: Get authenticated user's photo.
		'''
		response = PicovicoAPIRequest.get(urls.ME_PHOTO, headers=self.auth_headers)
		return response

	def upload_image(self, image_path, source=None):
		'''
			Picovico: Uploads the image to the current project
		'''
		return self.upload_image_file(image_path, source)

	def upload_image_file(self, file_path, source=None):
		'''
			Picovico: Checks if the image is uploaded locally and process the requests.
		'''
		if utils.is_local_file(file_path):
			response = PicovicoAPIRequest.put(urls.ME_PHOTO, file_path, headers=self.auth_headers)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = PicovicoAPIRequest.post(urls.ME_PHOTO, data=data, headers=self.auth_headers)
			return response

	def delete_image(self, image_id):
		'''
			Picovico: Deletes uploaded image
		'''
		return PicovicoAPIRequest.delete((urls.ME_PHOTO_DELETE).format(image_id), headers=self.auth_headers)

		