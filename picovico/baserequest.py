import collections

import requests
import six
from six.moves.urllib import parse

from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions


#: `RequestArg` namedtuple for PicovicoRequest 
RequestArg = collections.namedtuple('RequestArg', ('method', 'data'))


class PicovicoRequest(object):
    """ Picovico-SDK: Picovico Request class for API calls.

    This class is a convenience wrapper around `requests` module.
    It provides method calls and arguments for Picovico API. This also
    include URL buildup.
    
    Args:
        headers(dict): *Optional* headers to be included with API request.
    """

    def __init__(self, headers=None):
        super(PicovicoRequest, self).__init__()
        self.__host = pv_urls.PICOVICO_BASE
        self.__headers = headers
        self.__url = self.host

    @property
    def host(self):
        """ The base host URL. By default its provided by picovico.
        """
        return self.__host

    @host.setter
    def host(self, url):
        self.__host = url.lower()

    @property
    def url(self):
        """ The URL created  using host and path.
        """
        return self.__url

    @url.setter
    def url(self, endpoint):
        self.__url = parse.urljoin(self.host, endpoint)

    @property
    def headers(self):
        """ The header that is provided in init along with appends for additional headers.
        """
        return self.__headers

    @headers.setter
    def headers(self, value):
        if self.headers:
            self.__headers.update(value)
        else:
            self.__headers = value

    @staticmethod
    def get_request_args(method_name, req_data=None):
        """ Staticmethod to create common request arguments.

        This method creates data and method arguments for request call.

        Args:
            method_name(str): Supported method names such as 'get', 'post' etc.
            req_data(object): Data to be sent. Usually `dict` or open file.

        Returns:
            RequestArg: Object with `data` and `method` assigned.
        """
        args = {
            'method': method_name,
            'data': req_data
        }
        return RequestArg(**args)

    def is_authenticated(self, check_headers=None):
        """ Checks whether the object is authenticated or not.

        This method checks for header for authentication token and key.

        Returns:
            bool: *True* if header consist of authentication headers else *False*.
        """
        if not check_headers:
            check_headers = self.headers
        check = False
        if check_headers:
            check = all(k in check_headers and check_headers[k] for k in ('X-Access-Key', 'X-Access-Token'))
        return check

    def get(self, path):
        """ Request get method.

        Args:
            path(str): URL path.

        Raises:
            .PicovicoNotFound: If status is 404.
            .PicovicoUnauthorized: If status is 401.
            .PicovicoRequestError: If status is 400 related.
            .PicovicoServerError: If status is 500.

        Returns:
            dict: :mod:`json` data.
        """
        self.request_args = self.get_request_args('get')
        return self._respond(path)

    def post(self, path, post_data=None):
        """ Request post method.

        Args:
            path(str): URL path.
            post_data(dict): *Optional* Data to be posted `{'k': 'v'}` format.
        
        Raises:
            .PicovicoNotFound: If status is 404.
            .PicovicoUnauthorized: If status is 401.
            .PicovicoRequestError: If status is 400 related.
            .PicovicoServerError: If status is 500.
            AssertionError: when post_data is not :class:`dict`.

        Returns:
            dict: :mod:`json` data.
        """
        if post_data:
            assert isinstance(post_data, dict), 'data should be of {"key": "value"} format'
        self.request_args = self.get_request_args('post', post_data)
        return self._respond(path)

    def  put(self, path, filename=None, data_headers=None):
        """ Request put method.

        Args:
            path(str): URL path.
            filename(str): *Optional* filename with full path.
            data_headers(dict): *Optional* Data to be posted `{'k': 'v'}` format.
        
        Raises:
            .PicovicoNotFound: If status is 404.
            .PicovicoUnauthorized: If status is 401.
            .PicovicoRequestError: If status is 400 related.
            .PicovicoServerError: If status is 500.
            AssertionError: when filename or data_headers are provided but donot match the types.

        Returns:
            dict: :mod:`json` data.
        """
        if data_headers is not None:
            assert isinstance(data_headers, dict), 'data headers should be of {"key": "value"} format'
            self.headers = data_headers
        put_data = None
        if filename is not None:
            assert isinstance(filename, six.string_types), 'Filename should be valid name'
            put_data = open(filename, 'rb').read()
        self.request_args = self.get_request_args('put', req_data=put_data)
        return self._respond(path)

    def delete(self, path):
        """ Request put method.

        Args:
            path(str): URL path.

        Raises:
            .PicovicoNotFound: If status is 404.
            .PicovicoUnauthorized: If status is 401.
            .PicovicoRequestError: If status is 400 related.
            .PicovicoServerError: If status is 500.

        Returns:
            dict: :mod:`json` data.
        """
        self.request_args = self.get_request_args('delete')
        return self._respond(path)

    def _respond(self, path, headers=None):
        """ **Not for user.
        Appends path to URL and calls `requests` for API populating request arguments.
        Raises error  based on status.
        Return json data.

        Args:
            path(str): This should be path that was provided to method.
        """
        self.url = path
        request_args = self.request_args._asdict()
        request_args.update(url=self.url)
        if not headers:
            request_args.update(headers=self.headers)
        elif isinstance(headers, dict):
            request_args.update(headers=headers)
        response = requests.request(**request_args)
        try:
            json_response = response.json()
        except ValueError:
            json_response = {'message': response.text}
        if not response.ok:
            pv_exceptions.raise_valid_error(status_code=response.status_code, **json_response)
        return json_response
