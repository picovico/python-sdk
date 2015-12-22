from lib.api import PicovicoAPIRequest
from lib.auth.session import PicovicoSession
from lib import urls
from lib.helpers import check_video_data

class PicovicoStyle(PicovicoSession):
	'''
		Picovico: Library component for style.
	'''
	def get_styles(self):
		'''
			Picovico: Gets available styles
		'''
		return PicovicoAPIRequest.get(urls.GET_STYLES)

	def set_style(self, style_machine_name, video_id=None):
		'''
			Picovico: Defines style for the current video project.
		'''
		#self.video_id = None
		picovico_video = self.get(video_id)
		if style_machine_name:
			picovico_video['style'] = style_machine_name
			return True
		
		return False