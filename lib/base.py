import requests, json, sys
from lib import urls, utils, constants, exceptions
class PicovicoBase:

	def set_tokens(self, access_key, access_token):
		if access_key and access_token:
			self.access_key = access_key
			self.access_token = access_token
		else:
			raise exceptions.UserNotAuthenticated('Not authenticated. Please authenticate first')

	def picovico_auth_headers(self):
		return {
			"X-Access-Key":self.access_key,
			"X-Access-Token":self.access_token
		}

	def upload_image_file(self, file_path, source=None):
		if utils.is_local_file(file_path):
			return requests.put(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_PHOTO, file_path, headers=self.picovico_auth_headers())
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_PHOTO, data, headers=self.picovico_auth_headers())
			return json.loads(response.text)

	def upload_music_file(self, file_path, source=None):
		if utils.is_local_file(file_path):
			data = {
				'X-Music-Artist': "Unknown",
				"X-Music-Title": "Unknown - {}".format('r')
			}
			return requests.put(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_MUSIC, file_path, data, headers=self.picovico_auth_headers())
		else:
			data = {
				'url': file_path,
				'preview_url': file_path
			}
			response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_MUSIC, data, headers=self.picovico_auth_headers())
			return json.loads(response.text)


	def append_image_slide(self, vdd, image_id, caption=None):

		data = {
			'name': 'image',
			'data':{
				'text': caption,
			},
			'asset_id': image_id
		}
		self.append_vdd_slide(vdd, data)

	def append_vdd_slide(self, vdd, slide):

		if vdd:
			if not vdd['assets']:
				vdd['assets'] = []

			last_slide = None
			current_slides_count = len(vdd['assets'])
			last_end_time = 0

			if vdd['assets']:
				last_slide = vdd['assets'][len(vdd['assets']) - 1]

				if last_slide:
					last_end_time = last_slide["end_time"]
				else:
					last_end_time = last_slide.end_time

			slide['start_time'] = last_end_time
			slide['end_time'] = last_end_time + self.STANDARD_SLIDE_DURATION

			vdd['assets'].append(slide)


	def append_text_slide(self, vdd, title=None, text=None):
		'''
			Picovico: Prepares the slide data for text slides and appends to the vdd
		'''

		data = {
			'name': 'text',
			'data':{
				'title': title,
				'text': text
			}
		}
		self.append_vdd_slide(vdd, data)

	def set_music(self, vdd, music_id):
		'''
			Picovico:
				Saves music for the current video project.
     			Saved separately because only one music is supported.
		'''
		data = {
			'name': 'music',
			'asset_id': music_id,
			'_comment': 'Some cool comment which will replace later'
		}
		vdd['_music'] = data


	def append_music(self, vdd):
		'''
			Picovico: If music is set and not appended to the VDD slide, appends the music as vdd slide
		'''
		if vdd['_music']:
			self.append_vdd_slide(vdd, vdd['_music'])
			del vdd['_music']

	def reset_slides(self, vdd):
		vdd['assets'] = []

	def reset_music(self, vdd):
		del vdd['_music']


