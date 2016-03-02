import pytest

from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions
from picovico.components.base import PicovicoBaseComponent

@pytest.fixture(params=PicovicoBaseComponent._components)
def component(request):
    ret = {
        'name': request.param,
        'single': '{}_id'.format(request.param)
    }
    return ret

class TestBaseComponent:
    def test_create_request_args(self):
        req_args = PicovicoBaseComponent.create_request_args()
        assert 'url' in req_args and req_args['url'] == pv_urls.PICOVICO_STYLES
        assert 'method' in req_args and req_args['method'] == 'get'
        req_args = PicovicoBaseComponent.create_request_args(data='hello')
        assert 'data' in req_args
        req_args = PicovicoBaseComponent.create_request_args(method='post', url_attr='MY_STYLES')
        assert req_args['url'] == pv_urls.MY_STYLES
        assert req_args['method'] == 'post'
        with pytest.raises(AttributeError):
            PicovicoBaseComponent.create_request_args(url_attr='UNKNOWN')

    def test_component_methods(self, mock_obj, component, pv_request, method_calls, pv_urls):
        def ignore_not_implemented(func, *arg):
            try:
                func(*arg)
            except NotImplementedError:
                return False
            else:
                return True
        mocker = mock_obj.OBJ
        mr = mock_obj.REQUEST
        mocker.patch.multiple('picovico.components.base.PicovicoBaseComponent', __abstractmethods__=set())
        mc = mocker.patch('picovico.components.base.PicovicoBaseComponent.component', new_callable=mocker.PropertyMock)
        mc.return_value = component['name']
        pv_comp = PicovicoBaseComponent(pv_request.AUTH)
        if ignore_not_implemented(pv_comp.all):
            get_call = method_calls.GET_AUTH.copy()
            get_call.update(url=getattr(pv_urls, 'MY_{}S'.format(component['name'].upper())))
            mr.assert_called_with(**get_call)
        for meth in ('one', 'delete'):
            func = getattr(pv_comp, meth)
            if ignore_not_implemented(func, component['single']):
                method_call = method_calls.GET_AUTH
                if meth == 'delete':
                    method_call = getattr(method_calls, '{}_AUTH'.format(meth.upper()))
                method_call = method_call.copy()
                call_url = getattr(pv_urls, 'MY_SINGLE_{}'.format(component['name'].upper()))
                call_url_args = {'{}_id'.format(component['name']): component['single']}
                call_url = call_url.format(**call_url_args)
                method_call.update(url=call_url)
                mr.assert_called_with(**method_call)
