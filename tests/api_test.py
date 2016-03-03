import pytest

from picovico import PicovicoAPI
from picovico import exceptions as pv_exceptions

class TestPicovicoAPI:
    def test_auth_decoration(self, pv_mocks, pv_response, pv_act_request_args, pv_urls):
        request_mock  = pv_mocks.REQUEST
        calls = ('app_id', 'device_id', 'username', 'password')
        api = PicovicoAPI(*calls[:2])
        post_call = pv_act_request_args.POST.copy()
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            api.me()
        request_mock.return_value = pv_response.SUCCESS.AUTH
        api.login(*calls[2:])
        post_call.update(data=dict(zip(calls, calls)), url=pv_urls.PICOVICO_LOGIN)
        request_mock.assert_called_with(**post_call)
        api.me()
        me_call = pv_act_request_args.GET_AUTH.copy()
        me_call.update(url=pv_urls.ME)
        request_mock.assert_called_with(**me_call)


    def test_api_proxy(self):
        api = PicovicoAPI('app_id', 'device_id')
        assert api.app_id
        assert api.headers is None
        api.set_access_tokens("access_key", "access_token")
        assert api.headers
        assert api.is_authorized()
        api.logout()
        assert not api.is_authorized()

    def test_login_authenticate(self, pv_mocks, pv_response):
        request_mock = pv_mocks.REQUEST
        request_mock.return_value = pv_response.SUCCESS.AUTH
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.login('username', 'password')
        assert api.is_authorized()
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.is_authorized()
        api.authenticate('app_secret')
        assert api.is_authorized()
        
    def test_project_property(self, pv_mocks):
        mocker = pv_mocks.OBJ
        api = PicovicoAPI('app_id', 'device_id')
        assert not api.project
        mocker.patch.object(PicovicoAPI, 'is_authorized', return_value=True)
        mocker.patch('picovico.PicovicoRequest.is_authenticated', return_value=True)
        api = PicovicoAPI('app_id', 'device_id')
        assert api.project
