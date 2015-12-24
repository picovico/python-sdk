import unittest
from lib import config
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from lib.components.music import PicovicoMusic


class PicovicoMusicTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		self.account = PicovicoAccount(self.session)
		self.music = PicovicoMusic(self.session)

	def test_get_musics(self):
		'''
			Picovico: Test for music (GET)
		'''
		music = self.music.get_musics()
		#print(music)
		self.assertTrue('musics' in music.keys())

	def test_get_library_musics(self):
		'''
			Picovico: Test for library music (GET)
		'''
		library_musics = self.music.get_library_musics()
		self.assertTrue(library_musics is not None) 

	def test_delete_music(self):
		'''
			Picovico: Test for delete music (POST)
		'''
		del_music = self.music.delete_music('nMEwp')
		self.assertTrue('message' in del_music.keys())


if __name__ == '__main__':
	unittest.main()

