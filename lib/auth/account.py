from lib import urls
from lib.auth.session import PicovicoSession
from lib.api import PicovicoAPIRequest
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoAccount():

	picovico_session = None

	def __init__(self, picovico_session):
		try:
			if picovico_session:
				self.picovico_session = picovico_session
		except:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = PicovicoAPIRequest.get(url=urls.ME, headers=picovico_session.get_auth_headers())
		return response