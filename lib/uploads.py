from lib import utils, api, urls

class PicovicoUploads(api.PicovicoAPIRequest):

	def upload_image_file(self, file_path, source=None):
		if utils.is_local_file(file_path):
			response = self.put(urls.UPLOAD_PHOTO, file_path)
			return response
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = self.post(urls.UPLOAD_PHOTO, data=data)
			return response

	def upload_music_file(self, file_path, source=None):
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