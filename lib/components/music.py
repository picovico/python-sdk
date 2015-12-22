from lib.auth.session import PicovicoSession
from lib.api import PicovicoAPIRequest
from lib import utils, urls
from lib.helpers import check_video_data

class PicovicoMusic(PicovicoSession):
	'''
		Picovico: Library componenet for music
	'''
	def get_musics(self, headers=None):
		'''
			Picovico: List all the uploaded musics
		'''
		response = PicovicoAPIRequest.get(urls.GET_MUSICS, headers=headers)
		return response

	def get_library_musics(self, headers=None):
		'''
			Picovico: List all the library musics
		'''
		response = PicovicoAPIRequest.get(urls.GET_LIBRARY_MUSICS, headers=headers)
		return response

	def upload_music(self, music_path, source=None, headers=None):
		'''
			Picovico: Uploads the music file to the current project.
		'''
		return self.upload_music_file(music_path, source, headers=headers)

	def add_music(self, music_path, video_data=None, headers=None):
		'''
			Picovico: Defines the background music
		'''
		check_video_data(video_data)
		response = self.upload_music(music_path, headers=headers)

		if response['id']:
			self.add_library_music(response['id'], video_data)

		return response
		
	def upload_music_file(self, file_path, source=None, headers=None):
		'''
			Picovico: Checks if the music is uploaded locally and proecess the requests.
		'''
		if utils.is_local_file(file_path):
			data = {
				'Music-Artist': "Unknown",
				"Music-Title": "Unknown - {}".format('r')
			}
			response = PicovicoAPIRequest.put(urls.UPLOAD_MUSIC, file_path, data, headers=headers)
			return response
		else:
			data = {
				'url': file_path,
				'preview_url': file_path
			}
			response = PicovicoAPIRequest.post(urls.UPLOAD_MUSIC, data, headers=headers)
			return response

	def delete_music(self, music_id, headers=None):
		'''
			Picovico: Deletes the music from your library
		'''
		if music_id:
			response = PicovicoAPIRequest.delete((urls.DELETE_MUSIC).format(music_id), headers=headers)
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
