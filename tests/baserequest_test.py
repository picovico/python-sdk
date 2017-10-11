import six
import pytest
try:
    import mock
except ImportError:
    from unittest import mock

from picovico import urls
from picovico import exceptions as pv_exceptions
from picovico import constants as pv_constants
from picovico.baserequest import RequestArg, PicovicoRequest


class TestPicovicoRequest:
    def test_properties(self, pv_headers, pv_urls):
        pv_request = PicovicoRequest()
        assert pv_request.headers is None
        pv_request = PicovicoRequest(pv_headers.VALID)
        assert pv_request.headers == pv_headers.VALID
        assert pv_request.url == pv_request.host
        pv_request.headers = {'additional': "this is nothing."}
        assert 'X-VALID' in pv_request.headers and 'additional' in pv_request.headers
        pv_request.url = urls.ME
        assert pv_request.url == pv_urls.ME

    def test_get_request_args(self):
        req_args = PicovicoRequest.get_request_args('get')
        assert req_args and isinstance(req_args, RequestArg)
        assert req_args.method == 'get'
        assert req_args.data is None
        req_args = PicovicoRequest.get_request_args('post', 'Hello')
        assert req_args.method == 'post'
        assert req_args.data

    def test_respond(self, pv_mocks, pv_urls, pv_act_request_args, pv_response, pv_messages):
        request_mock = pv_mocks.REQUEST
        request_mock.return_value = pv_response.SUCCESS.OK
        pv_request = PicovicoRequest()
        pv_request.request_args = RequestArg(method='get', data=None)
        res = pv_request._respond(urls.ME)
        assert pv_request.url == pv_urls.ME
        get_call = pv_act_request_args.GET.copy()
        get_call.update(url=pv_urls.ME)
        request_mock.assert_called_with(**get_call)
        assert res == pv_messages.SUCCESS.OK
        request_mock.return_value = pv_response.ERROR.BAD
        with pytest.raises(pv_exceptions.PicovicoRequestError):
            pv_request._respond(urls.ME)

    @pytest.mark.parametrize('method', pv_constants.ALLOWED_METHODS)
    def test_methods(self, pv_mocks, pv_urls, method):
        mocker = pv_mocks.OBJ
        respond_mock = mocker.patch.object(PicovicoRequest, '_respond')
        pv_req = PicovicoRequest()
        method_func = getattr(pv_req, method)
        argument = {}
        data = None
        if method not in ('get', 'delete'):
            if method == 'post':
                argument.update(post_data='hello')
                with pytest.raises(AssertionError):
                    method_func(urls.ME, **argument)
                data = {'k': 'v'}
                argument.update(post_data=data)
            else:
                data = 'putdata'
                if six.PY2:
                    mocker.patch('picovico.baserequest.open', mock.mock_open(read_data=data))
                else:
                    mocker.patch('builtins.open', mock.mock_open(read_data=data))
                argument.update(filename='helo')
        method_func(urls.ME) if not argument else method_func(urls.ME, **argument)
        respond_mock.assert_called_with(urls.ME)
        assert pv_req.request_args.method == method
        assert pv_req.request_args.data == data
        
    def test_authentication_header(self, pv_headers):
        pv_req = PicovicoRequest()
        assert not pv_req.is_authenticated()
        header = pv_headers.VALID.copy()
        header.update({'X-Access-Key': 'Valid'})
        pv_req.headers = header
        assert not pv_req.is_authenticated()
        header.update({'X-Access-Token': None})
        assert not pv_req.is_authenticated()
        header.update({'X-Access-Token': 'Valid', 'X-Access-Key': None})
        assert not pv_req.is_authenticated()
        header.pop('X-Access-Token')
        header.update({'X-Access-Key': 'Valid'})
        assert not pv_req.is_authenticated()
        pv_req.headers = pv_headers.AUTH.copy()
        assert pv_req.is_authenticated()
