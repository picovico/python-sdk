from lib import urls, constants, exceptions, base

class PicovicoAPIRequest(object):

	def get_auth_headers(self, is_anonymous):
		if is_anonymous:
			headers = base.picovico_auth_headers()
		else:
			raise exceptions.PicovicoUnauthorizedException()


	def make_request(self, method, url, data, is_anonymous=False):
		response = requests.method(urls.PICOVICO_API_ENDPOINT + url, data, headers=get_auth_headers(is_anonymous))
		return self.decode_response(response)

	def sdk_response(response):
		decoded_response = json.loads(response.text)

		if not response.status_code == 200:
			error = decode_response['error']
			raise exceptions.PicovicoAPIResponseException(error['status'], error['message'], decode_response)

		return decode_response



