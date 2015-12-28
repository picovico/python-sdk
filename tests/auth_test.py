import requests, unittest, json
from lib import config, urls
from lib.auth.session import PicovicoSession
from lib.exceptions import DataNotFound, PicovicoAPIResponseException
from ddt import ddt, data, unpack
from lib.api import PicovicoAPIRequest

PICOVICO_USERNAME = "aaeronn.bhatta@gmail.com"
PICOVICO_PASSWORD = "aaeronn09"

@ddt
class PicovicoSessionTest(unittest.TestCase):

	@data(
			(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET, False, False),
			('fake-app-id', 'fake-app-secret', True, False),
		)
	@unpack
	def test_authenticate(self, app_id, app_secret, expectedPicovicoAPIResponseException, expectedDataNotFound):
		'''
			Picovico Test: Authentication test for picovico
		'''
		self.session = PicovicoSession(app_id, app_secret)

		if expectedPicovicoAPIResponseException:
			self.assertRaises(PicovicoAPIResponseException, lambda: self.session.authenticate())
			return 

		authenticate = self.session.authenticate()
		self.assertTrue(authenticate)

	@data(
			(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET),
		)
	@unpack
	def test_logout(self, app_id, app_secret):
		self.session = PicovicoSession(app_id, app_secret)
		logout = self.session.logout()
		self.assertTrue(logout)

	@data(
			(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET),
		)
	@unpack
	def test_login(self, app_id, app_secret):
		self.session = PicovicoSession(app_id, app_secret)
		login = self.session.login(PICOVICO_USERNAME, PICOVICO_PASSWORD, app_id)
		self.assertTrue(login)


if __name__ == '__main__':
	unittest.main()

