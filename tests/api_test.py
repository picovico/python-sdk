import pytest
from six.moves.urllib import parse

from picovico import PicovicoAPI
from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, mock_obj, response, method_calls, pv_urls):
        request_mock  = mock_obj.REQUEST
        calls = ('app_id', 'device_id', 'username', 'password')
        api = PicovicoAPI(*calls[:2])
        post_call = method_calls.POST.copy()
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        request_mock.return_value = response.SUCCESS.AUTH
        api.login(*calls[2:])
        post_call.update(data=dict(zip(calls, calls)), url=pv_urls.PICOVICO_LOGIN)
        request_mock.assert_called_with(**post_call)
        api.me()
        post_call = method_calls.GET_AUTH.copy()
        post_call.update(url=pv_urls.ME)
        request_mock.assert_called_with(**post_call)


    def test_api_proxy(self):
        api = PicovicoAPI('app_id', 'device_id')
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.headers
        assert api.is_authorized()
        api.logout()
        assert not api.is_authorized()

    def test_login_authenticate(self, mock_obj, response):
        request_mock = mock_obj.REQUEST
        request_mock.return_value = response.SUCCESS.AUTH
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.login('username', 'password')
        assert api.is_authorized()
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.authenticate('app_secret')
        assert api.is_authorized()
