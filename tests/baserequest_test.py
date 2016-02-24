import pytest
import mock
from six.moves.urllib import parse

from picovico import baserequest as api
from picovico import urls

class TestPicovicoRequest:
    def test_properties(self, response_messages):
        pv_api = api.PicovicoRequest()
        assert pv_api.headers is None
        pv_api = api.PicovicoRequest(response_messages['valid_header'])
        assert pv_api.headers == response_messages['valid_header']
        assert pv_api.endpoint == urls.PICOVICO_BASE
        pv_api.headers = {'additional': "this is nothing."}
        assert 'X-VALID' in pv_api.headers
        assert 'additional' in pv_api.headers
        pv_api.endpoint = urls.ME
        assert pv_api.endpoint == parse.urljoin(urls.PICOVICO_BASE, urls.ME)

    def test_request_args(self, response_messages):
        pv_api = api.PicovicoRequest(response_messages['valid_header'])
        args = pv_api._PicovicoRequest__get_args_for_url(urls.ME)
        assert 'headers' in args
        assert 'url' in args
        assert args['url'] == parse.urljoin(urls.PICOVICO_BASE, urls.ME)

    def test_api_methods(self, mocker, success_response, method_calls):
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = success_response
        pv_api = api.PicovicoRequest()
        assert pv_api.get(urls.ME) == success_response.json()
        get_call = method_calls.get('get').copy()
        get_call.update(url=parse.urljoin(urls.PICOVICO_BASE, urls.ME))
        mr.assert_called_with(**get_call)
        pv_api.post(urls.ME, data={'me': "myself"})
        post_call = method_calls.get('post').copy()
        post_call.update(url=parse.urljoin(urls.PICOVICO_BASE, urls.ME))
        post_call.update(data={'me': "myself"})
        mr.assert_called_with(**post_call)
        with pytest.raises(AssertionError):
            pv_api.post(urls.ME, data="hello")
        assert success_response.json() == pv_api.put(urls.ME)
        mocker.patch('picovico.baserequest.open', mock.mock_open(read_data='bibble'))
        pv_api.put(urls.ME, filename="fo", data_headers={'MUSIC_NAME': "Hello"}, )
        assert 'MUSIC_NAME' in pv_api.headers
        assert pv_api.request_args['method'] == 'put'
        assert 'data' in pv_api.request_args
        assert success_response.json() == pv_api.delete(urls.ME)
        
    def test_authentication_header(self, success_response):
        pv_req = api.PicovicoRequest()
        assert not pv_req.is_authenticated()
        header = {'X-Access-Key': None}
        pv_req.headers = header
        assert not pv_req.is_authenticated()
        header.update({'X-Access-Key': 'Valid'})
        assert not pv_req.is_authenticated()
        header.update({'X-Access-Token': None})
        assert not pv_req.is_authenticated()
        header.update({'X-Access-Token': 'Valid'})
        assert pv_req.is_authenticated()
        header.update({'X-Access-Token': None})
        assert not pv_req.is_authenticated()
