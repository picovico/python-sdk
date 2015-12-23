from lib import urls
from lib.api import PicovicoAPIRequest
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoAccount():

	picovico_session = None

	def __init__(self, picovico_session=None):

		if picovico_session:
			self.headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = PicovicoAPIRequest.get(url=urls.ME, headers=self.headers)
		return response