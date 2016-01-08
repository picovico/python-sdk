from lib import urls
from lib.api import PicovicoAPIRequest
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE


class PicovicoAccount():
	'''
		Picovico: Picovico class for user detail and updata.
	'''
	picovico_session = None

	def __init__(self, picovico_session=None):
		'''
			Picovico: Constructor to accept session instance. If not, will raise exception.
		'''
		if picovico_session:
			self.auth_headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def profile(self):
		'''
			Picovico: Generates profile for authenticated user
		'''
		response = PicovicoAPIRequest.get(url=urls.ME, headers=self.auth_headers)
		return response