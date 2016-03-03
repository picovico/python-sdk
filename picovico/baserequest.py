import collections

import requests
import six
from six.moves.urllib import parse

from . import urls as pv_urls
from . import exceptions as pv_exceptions


RequestArg = collections.namedtuple('RequestArg', ('method', 'data'))


class PicovicoRequest(object):
    '''
        Picovico: Picovico API Request methods.
        Args:
            headers(dict): (Optional)Header to attach for request
    '''
    def __init__(self, headers=None):
        self.__host = pv_urls.PICOVICO_BASE
        self.__headers = headers
        self.__url = self.host

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, url):
        self.__host = url.lower()

    @property
    def url(self):
        """
            Picovico: Read Only endpoint of API
        """
        return self.__url

    @url.setter
    def url(self, endpoint):
        self.__url = parse.urljoin(self.host, endpoint.lower())

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        if self.headers:
            self.__headers.update(value)
        else:
            self.__headers = value

    @staticmethod
    def get_request_args(method_name, req_data=None):
        args = {
            'method': method_name,
            'data': req_data
        }
        return RequestArg(**args)

    def is_authenticated(self):
        check = False
        if self.headers:
            check = all(k in self.headers and self.headers[k] for k in ('X-Access-Key', 'X-Access-Token'))
        return check
        
    def get(self, path):
        self.request_args = self.get_request_args('get')
        return self.__respond(path)

    def post(self, path, post_data):
        assert isinstance(post_data, dict), 'data should be of {"key": "value"} format'
        self.request_args = self.get_request_args('post', post_data)
        return self.__respond(path)

    def  put(self, path, filename=None, data_headers=None):
        if data_headers is not None:
            assert isinstance(data_headers, dict), 'data headers should be of {"key": "value"} format'
            self.headers = data_headers
        put_data = None
        if filename is not None:
            assert isinstance(filename, six.string_types), 'Filename should be valid name'
            with open(filename, 'r') as f:
                put_data = f
        self.request_args = self.get_request_args('put', put_data)
        return self.__respond(path)

    def delete(self, path):
        self.request_args = self.get_request_args('delete')
        return self.__respond(path)

    def __respond(self, path):
        '''
            Picovico: Returns json response.
            Checks if response is not 400 or 500.
            Raises error based on response status code.
        '''
        self.url = path
        request_args = self.request_args._asdict()
        request_args.update(url=self.url)
        request_args.update(headers=self.headers)
        response = requests.request(**request_args)
        json_response = response.json()
        if not response.ok:
            pv_exceptions.raise_valid_exceptions(status_code=response.status_code, **json_response)
        return json_response
