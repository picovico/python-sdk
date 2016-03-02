import pytest
import mock
from six.moves.urllib import parse

from picovico import baserequest as api
from picovico import urls

class TestPicovicoRequest:
    def test_properties(self, headers, pv_urls):
        pv_api = api.PicovicoRequest()
        assert pv_api.headers is None
        pv_api = api.PicovicoRequest(headers.VALID)
        assert pv_api.headers == headers.VALID
        assert pv_api.endpoint == urls.PICOVICO_BASE
        pv_api.headers = {'additional': "this is nothing."}
        assert 'X-VALID' in pv_api.headers
        assert 'additional' in pv_api.headers
        pv_api.endpoint = urls.ME
        assert pv_api.endpoint == pv_urls.ME

    def test_api_methods(self, response, method_calls, pv_urls, mock_obj):
        request_mock = mock_obj.REQUEST
        mocker = mock_obj.OBJ
        request_mock.return_value = response.SUCCESS.OK
        pv_api = api.PicovicoRequest()
        get_call = method_calls.GET.copy()
        get_call.update(url=pv_urls.ME)
        pv_api.get(url=urls.ME)
        request_mock.assert_called_with(**get_call)
        pv_api.post(urls.ME, post_data={'me': "myself"})
        post_call = method_calls.POST.copy()
        post_call.update(url=pv_urls.ME)
        post_call.update(data={'me': "myself"})
        request_mock.assert_called_with(**post_call)
        with pytest.raises(AssertionError):
            pv_api.post(urls.ME, post_data="hello")
        mocker.patch('picovico.baserequest.open', mock.mock_open(read_data='bibble'))
        pv_api.put(urls.ME, filename="fo", data_headers={'MUSIC_NAME': "Hello"}, )
        assert 'MUSIC_NAME' in pv_api.headers
        assert pv_api.request_args.method == 'put'
        assert pv_api.request_args.data

    def test_authentication_header(self):
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
