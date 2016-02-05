import abc

from .. import exceptions as pv_exceptions
from .. import urls as pv_urls
from .. import base as pv_base
from .. import decorators as pv_decorator


class PicovicoBaseComponent(object):
    """ Picovico Base Component class. (Abstract)
    This class is the base for all other component classes and shouldn't be used alone.

    Attributes:
        component(str): Name of component currently initiated.
    """
    __metaclass__ = abc.ABCMeta
    _names = ('get_{}', 'get_{}s', 'upload_{}_file', 'upload_{}_url', 'delete_{}', 'get_library_{}s')
    _components = ('style', 'music', 'photo', 'video')

    def _api_call(self, method='get', **request_args):
        assert method and method in ('get', 'post', 'put', 'delete'), 'Only "get", "post", "put" and "delete" allowed.'
        assert ('url' in request_args and request_args['url'])
        assert (request_args and len(request_args) < 3)
        return getattr(self._pv_request, method)(**request_args)

    def __init__(self, request_obj, name='video'):
        """ Authenticated request object for component access. """
        assert isinstance(request_obj, pv_base.PicovicoRequest)
        if name not in self._components:
            raise pv_exceptions.PicovicoComponentNotSupported('This component is not supported.')
        self.__component = name
        self._pv_request = request_obj
        for name in self._names:
            meth_name = name.format(self.component)
            setattr(self, meth_name, getattr(self, '_{}'.format(meth_name.replace(self.component, 'component'))))

    @property
    def component(self):
        return self.__component

    @pv_decorator.pv_not_implemented(_components[1:])
    @pv_decorator.pv_auth_required
    def _get_component(self, id):
        req_args = {
            'method': 'get',
            'url': getattr(pv_urls, 'MY_SINGLE_{}'.format(self.component.upper()), None),
            '{}_id'.format(id): id
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def _get_components(self):
        req_args = {
            'method': 'get',
            'url': getattr(pv_urls, 'MY_{}'.format(self.component.upper()))
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:3])
    @pv_decorator.pv_auth_required
    def _upload_component_file(self, filename, data_headers=None):
        req_args = {
            'method': 'put',
            'url': getattr(pv_urls, 'MY_{}'.format(self.component.upper())),
            'filename': filename,
            'data_headers': data_headers
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:3])
    @pv_decorator.pv_auth_required
    def _upload_component_url(self, url, **data):
        req_args = {
            'method': 'post',
            'url': getattr(pv_urls, 'MY_{}'.format(self.component.upper())),
            'data': dict(url=url, **data),
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:])
    @pv_decorator.pv_auth_required
    def _delete_component(self, id):
        req_args = {
            'method': 'get',
            'url': getattr(pv_urls, 'MY_SINGLE_{}'.format(self.component.upper())),
            '{}_id'.format(id): id
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[:2])
    def _get_library_components(self):
        req_args = {
            'method': 'get',
            'url': getattr(pv_urls, 'PICOVICO_{}S'.format(self.component.upper())),
        }
        return self._api_call(**req_args)
