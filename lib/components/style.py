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

	def set_style(self, style_machine_name, video_id=None):
		'''
			Picovico: Defines style for the current video project.
		'''
		pass
		#self.video_id = None
		# picovico_video = video_id
		# if style_machine_name:
		# 	picovico_video['style'] = style_machine_name
		# 	return True
		
		# return False