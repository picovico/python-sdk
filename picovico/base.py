import sys
import json

import requests
import six
from six.moves.urllib import parse

from . import urls as pv_urls
from . import exceptions as pv_exceptions

class PicovicoRequest(object):
    '''
        Picovico: Picovico API Request methods.
        Args:
            headers(dict): (Optional)Header to attach for request
    '''
    __endpoint = pv_urls.PICOVICO_BASE

    def __init__(self, headers=None):
        self.__headers = headers

    @property
    def endpoint(self):
        """
            Picovico: Read Only endpoint of API
        """
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, url):
        self.__endpoint = parse.urljoin(pv_urls.PICOVICO_BASE, url.lower())

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        if self.headers:
            self.__headers.update(value)
        else:
            self.__headers = value

    def __get_args_for_url(self, url):
        self.endpoint = url
        args =  {'url': self.endpoint}
        if self.headers:
            args.update(headers=self.headers)
        return args
    
    def is_authenticated(self):
        is_it = False
        if self.headers:
            access_keys_exists = 'X-Access-Key' in self.headers and 'X-Access-Token' in self.headers  
            access_values_exists = all((self.header['X-Access-Token'], self.headers['X-Access-Key']))
            if access_keys_exists and access_values_exists:
                is_it = True
        return is_it

    def get(self, url):
        self.request_args = self.__get_args_for_url(url)
        self.request_args.update(method='get')
        return self.__respond()

    def post(self, url, data):
        assert isinstance(data, dict), 'data should be of {"key": "value"} format'
        self.request_args = self.__get_args_for_url(url)
        self.request_args.update(data=data)
        self.request_args.update(method='post')
        return self.__respond()

    def  put(self, url, filename=None, data_headers=None):
        self.request_args = self.__get_args_for_url(url)
        if data_headers is not None:
            assert isinstance(data_headers, dict), 'data headers should be of {"key": "value"} format'
            self.headers = data_headers
        if filename is not None:
            assert isinstance(filename, six.string_types), 'Filename should be valid name'
            with open(filename, 'r') as f:
                self.request_args.update(data=f)
        self.request_args.update(method='put')
        return self.__respond()

    def delete(self, url):
        self.request_args = self.__get_args_for_url(url)
        self.request_args.update(method='delete')
        return self.__respond()

    def __respond(self):
        '''
            Picovico: Returns json response.
            Checks if response is not 400 or 500.
            Raises error based on response status code.
        '''
        response = requests.request(**self.request_args)
        json_response = response.json()
        if not response.ok:
            pv_exceptions.raise_valid_exceptions(status_code=response.status_code, **json_response)
        return json_response
