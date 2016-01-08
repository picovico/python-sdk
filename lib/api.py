import requests, json, sys
from lib import urls, constants, exceptions


class PicovicoAPIRequest:
	'''
		Picovico: Picovico API Request methods.
	'''

	@staticmethod
	def get(url=None, headers=None):
		'''
			Picovico: Performs get request. #GET()
		'''
		response = requests.get(urls.PICOVICO_API_ENDPOINT + url, headers=headers)
		return PicovicoAPIRequest.sdk_response(response)

	@staticmethod
	def post(url=None, data=None, headers=None):
		'''
			Picovico: Performs post request. #POST()
		'''
		response = requests.post(urls.PICOVICO_API_ENDPOINT + url, data, headers=headers)
		return PicovicoAPIRequest.sdk_response(response)

	@staticmethod
	def put(url=None, filename=None, data=None, headers=None):
		'''
			Picovico: Performs put request. #PUT()
		'''
		pv_file = open(filename, 'r')
		if data:
			headers.update(data)
		response = requests.put(urls.PICOVICO_API_ENDPOINT + url, pv_file, headers=headers)
		return PicovicoAPIRequest.sdk_response(response)

	@staticmethod
	def delete(url=None, headers=None):
		'''
			Picovico: Performs delete request. #DELETE()
		'''
		response = requests.delete(urls.PICOVICO_API_ENDPOINT + url, headers=headers)
		return PicovicoAPIRequest.sdk_response(response)

	@staticmethod
	def sdk_response(raw_response):
		'''
			Picovico: Decodes the raw response from api.
						Checks if status code is 200. If not raises PicovicoAPIResponseException with error message.
						Returns decoded response
		'''
		decoded_response = json.loads(raw_response.text)

		if not raw_response.status_code == 200:
			error = decoded_response['error']
			raise exceptions.PicovicoAPIResponseException(error['status'], error['message'], decoded_response)

		return decoded_response



