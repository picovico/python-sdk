import unittest
from lib import config
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from lib.exceptions import PicovicoSessionRequiredException


class PicovicoAccountTest(unittest.TestCase):

	def setUp(self):
		'''
			Picovico Test: Set up the app_id and app_secret and authenticate.
		'''
		self.session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
		self.authenticate = self.session.authenticate()
		try:
			self.account = PicovicoAccount()
		except PicovicoSessionRequiredException:
			self.account = PicovicoAccount(self.session)

	def test_profile(self):
		'''
			Picovico: Profile test for authenticated user
		'''
		profile = self.account.profile()
		self.assertTrue('id' in profile.keys())


if __name__ == '__main__':
	unittest.main()

