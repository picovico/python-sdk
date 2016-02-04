import mock
import pytest
from six.moves.urllib import parse

from picovico import PicovicoAPI
from picovico import urls as pv_urls
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, auth_response, method_calls):
        calls = ('app_id', 'device_id', 'username', 'password')
        api = PicovicoAPI(*calls[:2])
        post_call = method_calls.get('post').copy()
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = auth_response
            api.login(*calls[2:])
            post_call.update(data=dict(zip(calls, calls)), url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_LOGIN))
            mr.assert_called_with(**post_call)
            api.me()
            assert 'headers' in mr.call_args[1]

    def test_api_proxy(self, success_response, method_calls):
        api = PicovicoAPI('app_id', 'device_id')
        get_call = method_calls.get('get').copy()
        with mock.patch('picovico.base.requests.request') as mr:
            assert not api.is_authorized()
            mr.return_value = success_response
            api.get_library_musics()
            get_call.update(url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_MUSICS))
            mr.assert_called_with(**get_call)
            api.get_library_styles()
            get_call.update(url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_STYLES))
            mr.assert_called_with(**get_call)
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
