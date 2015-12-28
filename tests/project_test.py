import unittest
from lib import config, constants
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from project import PicovicoProject
from ddt import ddt, data, unpack
from lib.exceptions import VideoIdNotFound, PicovicoSessionRequiredException


PUBLISHED_VIDEO = 'nMFoh'

@ddt
class PicovicoProjectTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		authenticate = self.session.authenticate()

		try:
			self.project = PicovicoProject()
		except PicovicoSessionRequiredException:
			self.project = PicovicoProject(self.session)

		self.begin = self.project.begin("My Test Project")

	# @data((INITIAL_VIDEO,), (PUBLISHED_VIDEO,))
	# @unpack
	def test_open(self):
		open_project = self.project.open(self.begin['id'])
		self.assertTrue('id' in open_project.keys())

		open_project = self.project.open(PUBLISHED_VIDEO)
		self.assertFalse(open_project)
	# 	# try:
	# 	# 	self.assertTrue('id' in open_project.keys())
	# 	# except:
	# 	# 	self.assertFalse(open_project)


	@data(('vanilla', True), (None, False))
	@unpack
	def test_set_style(self, style_machine_name, ValidData):
		'''
			Picovico: Test projects' ste_style method 
		'''
		set_style = self.project.set_style(style_machine_name)

		if not ValidData:
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
		library_image = self.project.ProjectHelpers(self.project).add_library_image(None, vdd)
		self.assertFalse(library_image)


	@data(('title', 'text', True), (None, None, False))
	@unpack
	def test_add_text(self, title, text, ValidData):
		for i in range(0,2):

			if not ValidData:
				text = self.project.add_text(title, text)
				self.assertTrue(text is False)
				return 

			text = self.project.add_text(title, text)
			self.assertTrue(text is True)

	def test_add_music(self):
		music = self.project.add_music("https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Christmas-Rap.mp3")
		self.assertTrue('id' in music.keys())

	def test_add_library_music(self):
		vdd = {}
		library_music = self.project.ProjectHelpers(self.project).add_library_music(None, vdd)
		self.assertFalse(library_music)

	@data((None, None, False), ('Music', 'Aaeronn', True))
	@unpack
	def test_add_credits(self, title, text, ValidData):
		if not ValidData:
			credits = self.project.add_credits(title, text)
			self.assertTrue(credits is False)
			return 

		credits = self.project.add_credits(title, text)
		self.assertTrue(credits is True)

	def test_remove_credits(self):
		add_credits = self.project.add_credits("Music", "Aaeronn")
		remove_credits = self.project.remove_credits()
		try:
			self.assertTrue(remove_credits) 
		except:
			self.assertFalse(remove_credits)

	@data((constants.Q_360P, True), (None, False))
	@unpack
	def test_set_quality(self, quality, ValidData):
		if not ValidData:
			quality = self.project.set_quality(quality)
			return

		quality = self.project.set_quality(quality)
		self.assertTrue(quality)

	@data((True, False), (None, True))
	@unpack
	def test_create_video(self, video_id, expectedVideoIdNotFound):
		music = self.project.add_music("https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Christmas-Rap.mp3")
		set_style = self.project.set_style('vanilla')
		quality = self.project.set_quality(constants.Q_360P)

		for i in range(0,5):
			image = self.project.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
		
		if expectedVideoIdNotFound:
			self.assertRaises(VideoIdNotFound, lambda: self.project.create_video(video_id))
			return

		if video_id:
			create_video = self.project.create_video(self.begin['id'])
			self.assertTrue(create_video['status'] in [7102, 7101])

	def test_reset(self):
		music = self.project.add_music("https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Christmas-Rap.mp3")
		reset = self.project.reset()
		self.assertTrue('id' in reset.keys())

	def test_draft(self):
		draft = self.project.draft()
		self.assertTrue('id' in draft.keys())

	def test_dump(self):
		project = PicovicoProject(self.session)
		dump_false = project.dump()
		self.assertFalse(dump_false)

		dump = self.project.dump()
		self.assertTrue('id' in dump.keys())


	@data((True, True), (None, False))
	@unpack
	def test_preview_video(self, video_id, ValidData):
		for i in range(0,5):
			image = self.project.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
		music = self.project.add_music("https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Christmas-Rap.mp3")
		set_style = self.project.set_style('vanilla')
		quality = self.project.set_quality(constants.Q_360P)
		if not ValidData:
			self.assertRaises(VideoIdNotFound, lambda: self.project.preview_video(video_id))
			return 

		if video_id:
			prev_video = self.project.preview_video(self.begin['id'])
			return 

	@data((PUBLISHED_VIDEO, True), (None, False))
	@unpack
	def test_duplicate_video(self, video_id, ValidData):
		if not ValidData:
			self.assertRaises(VideoIdNotFound, lambda: self.project.duplicate_video(video_id))
			return 

		dup_video = self.project.duplicate_video(video_id)
		return 






if __name__ == '__main__':
	unittest.main()

