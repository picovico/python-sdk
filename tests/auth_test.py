import requests, sys
import unittest
import picovico
from lib import config

class PicovicoAuthenticationTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.app = picovico.Picovico(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		authenticate = self.app.authenticate()
		self.assertTrue('access_key' and 'access_token' in authenticate.keys())

	def test_authenticate(self):
		'''
			Picovico Test: As authentication is called in set up, it is no need to call explicitly here.
		'''
		# response = self.app.authenticate()
		# self.assertTrue('access_key' and 'access_token' in response.keys())
		pass

	def test_profile(self):
		'''
			Picovico Test: Test for picovico user profile.
		'''
		response = self.app.profile()
		self.assertTrue('email' in response.keys())

if __name__ == '__main__':
	unittest.main()

