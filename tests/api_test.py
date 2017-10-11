import pytest

from picovico import PicovicoAPI
from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:

    def test_api_proxy(self):
        api = PicovicoAPI('app_id', 'device_id')
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.auth_headers
        assert api.is_authorized()
        api.logout()
        assert not api.is_authorized()

    def test_login_authenticate(self, pv_mocks, pv_response):
        request_mock = pv_mocks.REQUEST
        request_mock.return_value = pv_response.SUCCESS.AUTH
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.authenticate('app_secret')
        assert api.is_authorized()
        res = api.authenticated_api(url=pv_urls.ME)
        assert request_mock.called
