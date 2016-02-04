import mock
import pytest

from picovico import PicovicoAPI
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, auth_response):
        api = PicovicoAPI('app_id', 'device_id')
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api.login('username', 'password')
            api.me()
        
    def test_api_proxy(self):
        api = PicovicoAPI('app_id', 'device_id')
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.headers

    def test_login_authenticate(self, auth_response):
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api = PicovicoAPI('app_id', 'device_id')
            api.login('username', 'password')
            assert api.headers
            assert 'X-Access-Key' in api.headers
            api.authenticate('app_secret')
            assert 'X-Access-Key' in api.headers

