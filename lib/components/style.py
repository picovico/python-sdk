from picovico.lib.api import PicovicoApiRequest

class PicovicoStyle(PicovicoApiRequest):
	'''
		Picovico: Library component for style.
	'''
	def get_styles(self):
		'''
			Picovico: Fetches styles available for the logged in account.
		'''
		response = self.get(urls.GET_STYLES)
		return response

	def set_style(self, style_machine_name):
		'''
			Picovico: Defines style for the current video project.
		'''
		if style_machine_name:
			self.vdd['style'] = style_machine_name
			return True
		
		return False
