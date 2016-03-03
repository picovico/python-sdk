import pytest

from picovico import urls
from picovico import constants as pv_constants
from picovico.components.base import PicovicoBaseComponent


@pytest.fixture(params=PicovicoBaseComponent._components)
def pv_component(request):
    ret = {
        'name': request.param,
        'single': '{}_id'.format(request.param)
    }
    return ret

def ignore_not_implemented(func, *arg, **kwargs):
    try:
        func(*arg, **kwargs)
    except NotImplementedError:
        return False
    else:
        return True

def common_mock_component(mocker, return_component, req):
    mocker.patch.multiple('picovico.components.base.PicovicoBaseComponent', __abstractmethods__=set())
    component_mock = mocker.patch('picovico.components.base.PicovicoBaseComponent.component', new_callable=mocker.PropertyMock)
    component_mock.return_value = return_component
    return PicovicoBaseComponent(req)

    
class TestBaseComponent:
    def test_create_request_args(self):
        req_args = PicovicoBaseComponent.create_request_args()
        assert 'path' in req_args and req_args['path'] == urls.PICOVICO_STYLES
        assert 'method' in req_args and req_args['method'] == 'get'
        req_args = PicovicoBaseComponent.create_request_args(data='hello')
        assert 'data' in req_args
        req_args = PicovicoBaseComponent.create_request_args(method='post', url_attr='MY_STYLES')
        assert req_args['path'] == urls.MY_STYLES
        assert req_args['method'] == 'post'
        with pytest.raises(AttributeError):
            PicovicoBaseComponent.create_request_args(url_attr='UNKNOWN')

    def test_component_methods(self, pv_mocks, pv_component, pv_request, pv_api_call_args):
        mocker = pv_mocks.OBJ
        api_call_mock = pv_mocks.API_CALL
        pv_comp = common_mock_component(mocker, pv_component['name'], pv_request.AUTH)
        for meth in ('get_library', 'all'):
            func = getattr(pv_comp, meth)
            if ignore_not_implemented(func):
                call_arg = pv_api_call_args.GET.copy()
                call_path = getattr(urls, 'MY_{}S'.format(pv_component['name'].upper()))
                call_arg.update(path=call_path)
                api_call_mock.assert_called_with(**call_arg)
        for meth in ('one', 'delete'):
            func = getattr(pv_comp, meth)
            if ignore_not_implemented(func, pv_component['single']):
                call_args = pv_api_call_args.GET
                if meth == 'delete':
                    call_arg = getattr(pv_api_call_args, '{}'.format(meth.upper()))
                call_arg = call_arg.copy()
                call_url = getattr(urls, 'MY_SINGLE_{}'.format(pv_component['name'].upper()))
                call_url_args = {'{}_id'.format(pv_component['name']): pv_component['single']}
                call_url = call_url.format(**call_url_args)
                call_arg.update(path=call_url)
                api_call_mock.assert_called_with(**call_arg)
        free_req = mocker.patch('picovico.components.base.pv_base.PicovicoRequest.get')
        if ignore_not_implemented(pv_comp.get_free):
            free_req.assert_called_with(path='{}s'.format(pv_component['name']))
            
    def test_component_methods_upload(self, pv_mocks, pv_component, pv_request, pv_api_call_args):
        mocker = pv_mocks.OBJ
        api_call_mock = pv_mocks.API_CALL
        pv_comp = common_mock_component(mocker, pv_component['name'], pv_request.AUTH)
        method_map = {
            'PUT': {
                'method': 'upload_file',
                'args': {
                    'filename': 'hello',
                    'data_headers': 'something'
                }
            }, 
            'POST': {
                'method': 'upload_url',
                'args': {
                    'url': 'someurl',
                    'extra': 'extra'
                }
            }
        }
        for call_method, meth in method_map.items():
            func = getattr(pv_comp, meth['method'])
            if ignore_not_implemented(func, **meth['args']):
                call_args = getattr(pv_api_call_args, call_method).copy()
                call_args.update(path='me/{}s'.format(pv_component['name']))
                if call_method == 'POST':
                    call_args.update(post_data=meth['args'])
                else:
                    call_args.update(meth['args'])
                api_call_mock.assert_called_with(**call_args)

    @pytest.mark.parametrize('method', pv_constants.ALLOWED_METHODS)
    def test_api_call(self, pv_method_mocks, pv_request, method):
        method_mock = getattr(pv_method_mocks, 'REQ_{}'.format(method.upper()), None)
        mocker = pv_method_mocks.OBJ
        pv_comp = common_mock_component(mocker, 'component', pv_request.AUTH)
        with pytest.raises(AssertionError):
            #non method error
            pv_comp._api_call('option')
        with pytest.raises(AssertionError):
            #only method and no path
            pv_comp._api_call(method)
        if method_mock:
            pv_comp._api_call(method, path=urls.ME)
            method_mock.assert_called_with(path=urls.ME)
            with pytest.raises(AssertionError):
                #more than 2 arguments
                pv_comp._api_call(path=urls.ME, junk='junk1', junk2='junk2', junk3='junk3')
            
