from lib.api import PicovicoApiRequest

class PicovicoMusic(PicovicoApiRequest):
	'''
		Picovico: Library componenet for music
	'''
	def upload_music(self, music_path, source=None, auth_session=None):
		'''
			Picovico: Uploads the music file to the current project.
		'''
		return self.upload_music_file(music_path, source, auth_session=auth_session)

	def upload_music_file(self, file_path, source=None, auth_session=None):
		'''
			Picovico: Checks if the music is uploaded locally and proecess the requests.
		'''
		if utils.is_local_file(file_path):
			data = {
				'Music-Artist': "Unknown",
				"Music-Title": "Unknown - {}".format('r')
			}
			response = self.put(urls.UPLOAD_MUSIC, file_path, data, auth_session=auth_session)
			return response
		else:
			data = {
				'url': file_path,
				'preview_url': file_path
			}
			response = self.post(urls.UPLOAD_MUSIC, data, auth_session=auth_session)
			return response

	def add_music(self, music_path, auth_session=None):
		'''
			Picovico: Defines the background music
		'''
		response = self.upload_music(music_path, auth_session=auth_session)

		if response['id']:
			self.add_library_music(response['id'])

		return response

	def add_library_music(self, music_id):
		'''
			Picovico: Define any previously uploaded music, or any music available from library. 
		'''
		if music_id:
			self.set_music(self.vdd, music_id)
			return False

		return True

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

	def delete_music(self, music_id):
		'''
			Picovico: Deletes the music from your library
		'''
		if music_id:
			response = self.delete((urls.DELETE_MUSIC).format(music_id))
			return response
		return False

	def get_music(self):
		pass

	def get_musics(self):
		'''
			Picovico: List all the uploaded musics
		'''
		response = self.get(urls.GET_MUSICS)
		return response

	def get_library_music(self, music_id=None):
		pass

	def get_library_musics(self):
		pass
