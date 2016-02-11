import pytest
from six.moves.urllib import parse

from picovico import PicovicoAPI
from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, mocker, auth_response, method_calls):
        calls = ('app_id', 'device_id', 'username', 'password')
        api = PicovicoAPI(*calls[:2])
        post_call = method_calls.get('post').copy()
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = auth_response
        api.login(*calls[2:])
        post_call.update(data=dict(zip(calls, calls)), url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_LOGIN))
        assert mr.call_args[1] == post_call
        api.me()
        #mr.assert_called_with(**post_call)
        assert 'headers' in mr.call_args[1]

    def test_api_proxy(self):
        api = PicovicoAPI('app_id', 'device_id')
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.headers
        assert api.is_authorized()
        api.logout()
        assert not api.is_authorized()

    def test_login_authenticate(self, mocker, auth_response):
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = auth_response
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.login('username', 'password')
        assert api.is_authorized()
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = auth_response
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.authenticate('app_secret')
        assert api.is_authorized()
