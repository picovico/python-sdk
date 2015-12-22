from lib import urls
from lib.auth.session import PicovicoSession
from lib.api import PicovicoAPIRequest
from lib.exceptions import PicovicoSessionRequiredException

class PicovicoAccount():

	picovico_session = None

	def __init__(self, picovico_session):
		if picovico_session is None:
			raise PicovicoSessionRequiredException()
		self.picovico_session = picovico_session

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = PicovicoAPIRequest.get(url=urls.ME, headers=picovico_session.get_auth_headers())
		return response