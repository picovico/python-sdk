from picovico.lib.api import PicovicoApiRequest

class PicovicoPhoto(PicovicoApiRequest):
	'''
		Picovico: Library componenet for photo
	'''
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

	def add_image(self, image_path, caption="", source="hosted", auth_session=None):
		'''
			Picovico: Add and append image to the current project
		'''
		response = self.upload_image(image_path, source, auth_session=auth_session)
		if response['id']:
			self.add_library_image(response['id'], caption)

		return response

	def add_library_image(self, image_id, caption=""):
		'''
			Picovico: Appends any image previously uploaded.
		'''
		if image_id:
			self.append_image_slide(self.vdd, image_id, caption)
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
		self.append_vdd_slide(vdd, data)

	def add_text(self, title="", text=""):
		'''
			Picovico: Adds text slide to the project
		'''
		if title or text:
			self.append_text_slide(self.vdd, title, text)
			return True
		
		return False

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
		
	def get_photos(self):
		pass