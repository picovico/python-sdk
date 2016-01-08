import os
import unittest
from ddt import ddt, data, unpack
from lib import config
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from lib.components.music import PicovicoMusic
from lib.components.photo import PicovicoPhoto
from lib.components.style import PicovicoStyle
from lib.components.video import PicovicoVideo
from lib.exceptions import PicovicoSessionRequiredException, VideoIdNotFound

MUSIC_ID = 'nMEwp'
IMAGE_ID = "nMEoM"
VIDEO_ID = "nMFoG"

#TEST_DATA_DIR =  os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/data/"
TEST_DATA_DIR =  os.path.realpath(__file__)
TEST_BASE_DIR = os.path.dirname(TEST_DATA_DIR) + "/data/"
print(TEST_BASE_DIR)

LOCAL_MUSIC_FILE =  TEST_BASE_DIR + "music.mp3"
LOCAL_IMAGE_FILE = TEST_BASE_DIR + "image.jpg"

URL_MUSIC_FILE = "https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Angels-We-Have-Heard-piano.mp3"
URL_IMAGE_FILE = "https://s3-us-west-2.amazonaws.com/pv-styles/carol/carol_thumb.jpg"

@ddt
class PicovicoMusicTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		try:
			self.music = PicovicoMusic()
		except PicovicoSessionRequiredException:
			self.music = PicovicoMusic(self.session)

	def test_get_musics(self):
		'''
			Picovico: Test for music (GET)
		'''
		music = self.music.get_musics()
		self.assertTrue('musics' in music.keys())

	def test_get_library_musics(self):
		'''
			Picovico: Test for library music (GET)
		'''
		library_musics = self.music.get_library_musics()
		self.assertTrue(library_musics is not None) 

	@data((URL_MUSIC_FILE,),(LOCAL_MUSIC_FILE,))
	@unpack
	def test_upload_music(self, music_file):
		upload_music = self.music.upload_music(music_file)
		return 

	@data((MUSIC_ID, True), (None, False))
	@unpack
	def test_delete_music(self, music_id, ValidData):
		'''
			Picovico: Test for delete music (POST)
		'''
		if not ValidData:
			del_music = self.music.delete_music(music_id)
			self.assertFalse(del_music)

		del_music = self.music.delete_music('nMEwp')
		self.assertTrue('message' in del_music.keys())


@ddt
class PicovicoPhotoTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		try:
			self.photo = PicovicoPhoto()
		except PicovicoSessionRequiredException:
			self.photo = PicovicoPhoto(self.session)

	def test_get_images(self):
		images = self.photo.get_images()
		self.assertTrue(images is not None)
		return

	@data((URL_IMAGE_FILE,),(LOCAL_IMAGE_FILE,))
	@unpack
	def test_upload_image(self, image_file):
		upload_image = self.photo.upload_image(image_file, source="hosted")
		return

	@data((IMAGE_ID, True), (None, False))
	@unpack
	def test_delete_image(self, image_id, ValidData):
		if not ValidData:
			try:
				del_image = self.photo.delete_image(image_id)
				self.assertFalse(del_image)
			except:
				return False
		try:
			del_image = self.photo.delete_image(image_id)
			self.assertTrue('message' in del_image.keys())
		except:
			return False


@ddt
class PicovicoStyleTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		try:
			self.style = PicovicoStyle()
		except PicovicoSessionRequiredException:
			self.style = PicovicoStyle(self.session)

	def test_get_styles(self):
		style = self.style.get_styles()
		self.assertTrue(style is not None)


@ddt
class PicovicoVideoTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		try:
			self.video = PicovicoVideo()
		except PicovicoSessionRequiredException:
			self.video = PicovicoVideo(self.session)

	@data((VIDEO_ID, True), (None, False))
	@unpack
	def test_get_video(self, video_id, ValidData):
		if not ValidData:
			self.assertRaises(VideoIdNotFound, lambda: self.video.get_video(video_id))
			return 

		video = self.video.get_video(video_id)
		self.assertEqual(video['status'], 7102)

	def test_get_videos(self):
		videos = self.video.get_videos()
		self.assertTrue(videos is not None)

if __name__ == '__main__':
	unittest.main()

