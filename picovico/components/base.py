import abc

from picovico import urls as pv_urls
from picovico import constants as pv_constants
from picovico import baserequest as pv_request
from picovico import decorators as pv_decorators


class PicovicoBaseComponent(object):
    """ Picovico-SDK: Abstract class for Picovico Components.

    Abstract class with common component methods and API calls.

    """
    __metaclass__ = abc.ABCMeta
    _components = ('style', 'music', 'photo', 'video')


    def __init__(self, request_obj):
        """
        Args:
            request_obj(.PicovicoRequest): instance of :class:`.PicovicoRequest`.

        Raises:
            AssertionError
        """
        assert isinstance(request_obj, pv_request.PicovicoRequest)
        self._pv_request = request_obj

    @staticmethod
    def create_request_args(**kwargs):
        """ staticmethod to create common request argument such as methods and paths.
        """
        url_attr = kwargs.pop('url_attr', 'PICOVICO_STYLES')
        if 'method' not in kwargs:
            kwargs.update(method='get')
        req_url = getattr(pv_urls, url_attr)
        kwargs.update(path=req_url)
        return kwargs

    def _api_call(self, method='get', **request_args):
        """ **Not for User.
        Actual request call.
        """
        assert method and method in pv_constants.ALLOWED_METHODS, 'Only {} allowed.'.format(','.join(pv_constants.ALLOWED_METHODS))
        assert ('path' in request_args and request_args['path'])
        assert (1 <= len(request_args) <= 3)
        return getattr(self._pv_request, method)(**request_args)

    @abc.abstractproperty
    def component(self):
        """ Abstract component.
        This will be overridden by allowed components for specific class.
        """
        raise NotImplementedError

    def __sanitize_single_url(self, url, url_args):
        return url.format(**url_args)

    @pv_decorators.pv_not_implemented(_components[1:])
    @pv_decorators.pv_auth_required
    def one(self, id):
        """ Fetch one with specific id.

        Args:
            id(str): id to fetch.
        """
        url_args =  {'{}_id'.format(self.component): id}
        req_args = self.create_request_args(**{
            'method': 'get',
            'url_attr': 'MY_SINGLE_{}'.format(self.component.upper()),
        })
        req_args.update(path=self.__sanitize_single_url(req_args.pop('path'), url_args))
        return self._api_call(**req_args)

    @pv_decorators.pv_auth_required
    def all(self):
        """ Fetch all.
        """
        req_args = self.create_request_args(**{
            'method': 'get',
            'url_attr': 'MY_{}S'.format(self.component.upper())
        })
        return self._api_call(**req_args)

    @pv_decorators.pv_not_implemented(_components[1:3])
    @pv_decorators.pv_auth_required
    def upload_file(self, filename, data_headers=None):
        """ Upload file.

        Args:
            filname(str): path to file.
            data_headers(dict): *Optional* Any additional headers.
        """
        req_args = self.create_request_args(**{
            'method': 'put',
            'url_attr': 'MY_{}S'.format(self.component.upper()),
            'filename': filename
        })
        if data_headers:
            req_args.update(data_headers=data_headers)
        return self._api_call(**req_args)

    @pv_decorators.pv_not_implemented(_components[1:3])
    @pv_decorators.pv_auth_required
    def upload_url(self, url, **data):
        """ Upload URL.

        Args:
            url(str): URL to upload.
            keyargs: Any additional data.
        """
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_{}S'.format(self.component.upper()),
            'post_data': dict(url=url, **data),
        })
        return self._api_call(**req_args)

    @pv_decorators.pv_not_implemented(_components[1:])
    @pv_decorators.pv_auth_required
    def delete(self, id):
        """ Remove specific.

        Args:
            id(str): id to be removed.
        """
        url_args =  {'{}_id'.format(self.component): id}
        req_args = self.create_request_args(**{
            'method': 'delete',
            'url_attr': 'MY_SINGLE_{}'.format(self.component.upper()),
        })
        req_args.update(path=self.__sanitize_single_url(req_args.pop('path'), url_args))
        return self._api_call(**req_args)

    #@pv_decorators.pv_not_implemented(_components[:2])
    #@pv_decorators.pv_auth_required
    #def get_library(self):
        #""" Helper method to fetch all user component data.
        #This method is similar to `all`.
        #"""
        #req_args = self.create_request_args(**{
            #'method': 'get',
            #'url_attr': 'MY_{}S'.format(self.component.upper()),
        #})
        #return self._api_call(**req_args)

    @pv_decorators.pv_not_implemented(_components[:2])
    def get_free(self):
        """ View Picovico free components.
        """
        free_req = pv_request.PicovicoRequest()
        return free_req.get(path=getattr(pv_urls, 'PICOVICO_{}S'.format(self.component.upper())))
