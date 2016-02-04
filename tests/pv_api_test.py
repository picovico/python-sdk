import mock
import pytest
from six.moves.urllib import parse

from picovico import PicovicoAPI
from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, auth_response):
        calls = ('app_id', 'device_id', 'username', 'password')
        api = PicovicoAPI(*calls[:2])
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api.login(*calls[2:])
            mr.assert_called_with(data=dict(zip(calls, calls)), method='post', url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_LOGIN))
            api.me()
            assert 'headers' in mr.call_args[1]
                    
    def test_api_proxy(self, success_response):
        api = PicovicoAPI('app_id', 'device_id')
        with mock.patch('picovico.base.requests.request') as mr:
            assert not api.is_authorized()
            mr.return_value = success_response
            api.get_library_musics()
            mr.assert_called_with(method='get', url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_MUSICS))
            api.get_library_styles()
            mr.assert_called_with(method='get', url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_STYLES))
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.headers
        assert api.is_authorized()
        api.logout()
        assert not api.is_authorized()
    
    def test_login_authenticate(self, auth_response):
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api = PicovicoAPI('app_id', 'device_id')
            assert not api.is_authorized()
            api.login('username', 'password')
            assert api.is_authorized()
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api = PicovicoAPI('app_id', 'device_id')
            assert not api.is_authorized()
            api.authenticate('app_secret')
            assert api.is_authorized()
