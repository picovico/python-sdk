from lib.api import PicovicoAPIRequest
from lib.auth.session import PicovicoSession
from lib import urls, exceptions, messages
from lib.exceptions import PicovicoSessionRequiredException
from lib.messages import SESSION_REQUIRED_MESSAGE

class PicovicoStyle():
	'''
		Picovico: Library component for style.
	'''
	picovico_session = None

	def __init__(self, picovico_session=None):

		if picovico_session:
			self.headers = picovico_session.get_auth_headers()
		else:
			raise PicovicoSessionRequiredException(SESSION_REQUIRED_MESSAGE)

	def get_styles(self):
		'''
			Picovico: Gets available styles
		'''
		return PicovicoAPIRequest.get(urls.GET_STYLES, headers=self.headers)
