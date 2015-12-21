from lib.api import PicovicoAPIRequest
from lib import urls
from lib.helpers import check_video_data

class PicovicoStyle(PicovicoAPIRequest):
	'''
		Picovico: Library component for style.
	'''
	def get_styles(self, auth_session=None):
		'''
			Picovico: Gets available styles
		'''
		return self.get(urls.GET_STYLES, auth_session=auth_session)

	def set_style(self, style_machine_name, video_data=None):
		'''
			Picovico: Defines style for the current video project.
		'''
		check_video_data(video_data)
		if style_machine_name:
			video_data['style'] = style_machine_name
			return True
		
		return False