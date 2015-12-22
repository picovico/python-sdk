from lib import urls
from lib.api import PicovicoAPIRequest

class PicovicoAccount(PicovicoAPIRequest):

	def profile(self, auth_session=None):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = self.get(url=urls.ME, auth_session=auth_session)
		return response