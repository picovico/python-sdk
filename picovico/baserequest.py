import sys
import json
import collections

import requests
import six
from six.moves.urllib import parse

from . import urls as pv_urls
from . import exceptions as pv_exceptions

RequestArg = collections.namedtuple('RequestArg', ('method', 'data', 'headers', 'url'))

class PicovicoRequest(object):
    '''
        Picovico: Picovico API Request methods.
        Args:
            headers(dict): (Optional)Header to attach for request
    '''
    __base = pv_urls.PICOVICO_BASE

    def __init__(self, headers=None):
        self.__headers = headers
        self.__endpoint = self.base_url

    @property
    def base_url(self):
        return self.__base

    @base_url.setter
    def base_url(self, url):
        self.__base = url.lower()

    @property
    def endpoint(self):
        """
            Picovico: Read Only endpoint of API
        """
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, url):
        self.__endpoint = parse.urljoin(self.base_url, url.lower())

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        if self.headers:
            self.__headers.update(value)
        else:
            self.__headers = value

    def __get_args_for_url(self, method_name, url, data=None):
        self.endpoint = url
        args =  {'url': self.endpoint, 'data': data}
        args.update(method=method_name)
        args.update(headers=self.headers)
        return RequestArg(**args)

    def is_authenticated(self):
        check = False
        if self.headers:
            check = all(k in self.headers and self.headers[k] for k in ('X-Access-Key', 'X-Access-Token'))
        return check
        
    def get(self, url):
        self.request_args = self.__get_args_for_url('get', url)
        return self.__respond()

    def post(self, url, post_data):
        assert isinstance(post_data, dict), 'data should be of {"key": "value"} format'
        self.request_args = self.__get_args_for_url('post', url, data=post_data)
        return self.__respond()

    def  put(self, url, filename=None, data_headers=None):
        if data_headers is not None:
            assert isinstance(data_headers, dict), 'data headers should be of {"key": "value"} format'
            self.headers = data_headers
        put_data = None
        if filename is not None:
            assert isinstance(filename, six.string_types), 'Filename should be valid name'
            with open(filename, 'r') as f:
                put_data = f
        self.request_args = self.__get_args_for_url('put', url, data=put_data)
        return self.__respond()

    def delete(self, url):
        self.request_args = self.__get_args_for_url('delete', url)
        return self.__respond()

    def __respond(self):
        '''
            Picovico: Returns json response.
            Checks if response is not 400 or 500.
            Raises error based on response status code.
        '''
        request_args = self.request_args._asdict()
        response = requests.request(**request_args)
        json_response = response.json()
        if not response.ok:
            pv_exceptions.raise_valid_exceptions(status_code=response.status_code, **json_response)
        return json_response
