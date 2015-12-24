import unittest
from lib import config, constants
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from project import PicovicoProject
from ddt import ddt, data, unpack
from lib.exceptions import VideoIdNotFound

INITIAL_VIDEO = 'nMFoG'
PUBLISHED_VIDEO = 'nMFoh'

@ddt
class PicovicoProjectTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		authenticate = self.session.authenticate()
		self.project = PicovicoProject(self.session)
		self.begin = self.project.begin("My Test Project")


	@data((INITIAL_VIDEO,), (PUBLISHED_VIDEO,))
	@unpack
	def test_open(self, video_id):
		open_project = self.project.open(video_id)
		try:
			self.assertTrue('id' in open_project.keys())
		except:
			self.assertFalse(open_project)


	@data(('vanilla', False), (None, True))
	@unpack
	def test_set_style(self, style_machine_name, expectedFalse):
		'''
			Picovico: Test projects' ste_style method 
		'''
		set_style = self.project.set_style(style_machine_name)

		if expectedFalse:
			set_style = self.project.set_style(style_machine_name)
			self.assertTrue(set_style is False)
			return 

		self.assertTrue(set_style is True)

	def test_add_image(self):
		for i in range(0,2):
			image = self.project.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
			self.assertTrue('id' in image.keys())

	def test_add_library_image(self):
		vdd = {}
		library_image = self.project.add_library_image(None, vdd)
		self.assertFalse(library_image)


	@data(('title', 'text', False), (None, None, True))
	@unpack
	def test_add_text(self, title, text, expectedFalse):
		for i in range(0,2):

			if expectedFalse:
				text = self.project.add_text(title, text)
				self.assertTrue(text is False)
				return 

			text = self.project.add_text(title, text)
			self.assertTrue(text is True)

	def test_add_music(self):
		music = self.project.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3")
		self.assertTrue('id' in music.keys())

	def test_add_library_music(self):
		vdd = {}
		library_music = self.project.add_library_music(None, vdd)
		self.assertFalse(library_music)

	@data(('Music', 'Aaeronn', False), (None, None, True))
	@unpack
	def test_add_credits(self, title, text, expectedFalse):
		if expectedFalse:
			credits = self.project.add_credits(title, text)
			self.assertTrue(credits is False)
			return 

		credits = self.project.add_credits(title, text)
		self.assertTrue(credits is True)

	def test_remove_credits(self):
		remove_credits = self.project.remove_credits()
		try:
			self.assertTrue(remove_credits)
			return 
		except:
			self.assertFalse(remove_credits)

	@data((constants.Q_360P, False), (None, True))
	@unpack
	def test_set_quality(self, quality, expectedFalse):
		if expectedFalse:
			quality = self.project.set_quality(quality)
			return

		quality = self.project.set_quality(quality)
		self.assertTrue(quality)

	@data((INITIAL_VIDEO, False), (None, True))
	@unpack
	def test_create_video(self, video_id, expectedVideoIdNotFound):
		if expectedVideoIdNotFound:
			self.assertRaises(VideoIdNotFound, lambda: self.project.create_video(video_id))
			return

		create_video = self.project.create_video(video_id)
		return

	def test_reset(self):
		reset = self.project.reset()
		self.assertTrue('id' in reset.keys())

	def test_draft(self):
		draft = self.project.draft()
		self.assertTrue('id' in draft.keys())

	def test_dump(self):
		dump = self.project.dump()
		self.assertTrue('id' in dump.keys())



if __name__ == '__main__':
	unittest.main()

