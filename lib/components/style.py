from lib.api import PicovicoAPIRequest
from lib import urls

class PicovicoStyle(PicovicoAPIRequest):
	'''
		Picovico: Library component for style.
	'''
	def get_styles(self, auth_session):
		'''
			Picovico: Fetches styles available for the logged in account.
		'''
		response = self.get(urls.GET_STYLES, auth_session=auth_session)
		return response

	# def set_style(self, style_machine_name, vdd):
	# 	'''
	# 		Picovico: Defines style for the current video project.
	# 	'''
	# 	if style_machine_name:
	# 		vdd['style'] = style_machine_name
	# 		return True
		
	# 	return False
