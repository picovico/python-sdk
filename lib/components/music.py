from lib.api import PicovicoAPIRequest
from lib import utils, urls

class PicovicoMusic(PicovicoAPIRequest):
	'''
		Picovico: Library componenet for music
	'''
	def get_musics(self, auth_session):
		'''
			Picovico: List all the uploaded musics
		'''
		response = self.get(urls.GET_MUSICS, auth_session=auth_session)
		return response

	def get_library_musics(self, auth_session):
		'''
			Picovico: List all the library musics
		'''
		response = self.get(urls.GET_LIBRARY_MUSICS, auth_session=auth_session)
		return response
		
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

	def delete_music(self, music_id):
		'''
			Picovico: Deletes the music from your library
		'''
		if music_id:
			response = self.delete((urls.DELETE_MUSIC).format(music_id))
			return response
		return False

	def add_library_music(self, music_id, vdd):
		'''
			Picovico: Define any previously uploaded music, or any music available from library. 
		'''
		if music_id:
			self.set_music(music_id, vdd)
			return False
			
		return True

	def set_music(self, music_id, vdd):
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
