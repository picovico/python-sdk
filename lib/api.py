import requests, json, sys
from lib import urls, constants, exceptions
#from lib.session import is_logged_in

class PicovicoAPIRequest:

	def is_logged_in(self, auth_session):
		if auth_session.get('X-Access-Key') and auth_session.get('X-Access-Token'):
			return True

		return False

	def get_auth_headers(self, is_anonymous, auth_session):
		'''
		Picovico: Checks if user is anonymous and returns exceptis if it is.
		'''
		if is_anonymous:
			return {
			"X-Access-Key":None,
			"X-Access-Token":None
		}
		if not is_anonymous and not self.is_logged_in(auth_session):
			raise exceptions.PicovicoUnauthorizedException()

		return auth_session

	def get(self, url=None, is_anonymous=False, auth_session=None):
		# headers = lambda auth_session: auth_session if auth_session else self.get_auth_headers(is_anonymous)
		
		response = requests.get(urls.PICOVICO_API_ENDPOINT + url, headers=self.get_auth_headers(is_anonymous, auth_session))
		return self.sdk_response(response)

	def post(self, url=None, data=None, is_anonymous=False, auth_session=None):
		response = requests.post(urls.PICOVICO_API_ENDPOINT + url, data, headers=self.get_auth_headers(is_anonymous, auth_session))
		# response = requests.post(urls.PICOVICO_API_ENDPOINT + url, data)
		return self.sdk_response(response)

	def put(self, url=None, filename=None, data=None, is_anonymous=False, auth_session=None):
		response = requests.put(urls.PICOVICO_API_ENDPOINT + url, filename, data, headers=self.get_auth_headers(is_anonymous, auth_session))
		return self.sdk_response(response)

	# def delete(self, url=None, is_anonymous=False):
	# 	response = requests.delete(urls.PICOVICO_API_ENDPOINT + url, headers=self.get_auth_headers(is_anonymous))
	# 	return self.sdk_response(response)

	def sdk_response(self, response):
		decoded_response = json.loads(response.text)

		if not response.status_code == 200:
			error = decoded_response['error']
			raise exceptions.PicovicoAPIResponseException(error['status'], error['message'], decoded_response)

		return decoded_response


